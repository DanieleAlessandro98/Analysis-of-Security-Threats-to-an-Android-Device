import os
from PyQt5.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import utils
from errors import AnalyzerError
from backend.mobsf_api_handler import MobSFAPIHandler
from backend.analysis_result import AnalysisResult

class ApkAnalyzer(QThread):
    analysis_result = AnalysisResult()

    current_package_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    completed_signal = pyqtSignal(int, dict, list, dict)

    def run(self):
        utils.create_folder(utils.SCAN_RESULT_FOLDER)
        self.mobsf_instance = MobSFAPIHandler()
        self.stopped = False

        self.process_packages()

    def stop_analysis(self):
        self.stopped = True

    def upload_file(self, file_path):
        upload = self.mobsf_instance.upload(file_path)
        return upload

    def scan_file(self, file_path, upload_hash):
        scan = self.mobsf_instance.scan(file_path, upload_hash)
        return scan

    def delete_scan(self, upload_hash):
        delete_scan = self.mobsf_instance.delete_scan(upload_hash)
        return delete_scan

    def generate_report_pdf(self, upload_hash, pdf_name):
        report = self.mobsf_instance.report_pdf(upload_hash, pdf_name)
        return report

    def generate_report_json(self, upload_hash):
        report = self.mobsf_instance.report_json(upload_hash)
        return report

    def get_security_score(self, upload_hash):
        scorecard = self.mobsf_instance.scorecard(upload_hash)
        return scorecard.get("security_score", None)

    def process_packages(self):
        packages = utils.get_package_files()

        total_packages = len(packages)
        completed_packages = 0

        with ThreadPoolExecutor(max_workers=1) as executor:
            for package in packages:
                if self.stopped:
                    break
                
                file = utils.get_package_output_path(package)
                self.current_package_signal.emit(f"{os.path.splitext(os.path.basename(file))[0]}")

                future = executor.submit(self.process_package, file)

                try:
                    future.result(timeout=60*60)
                except TimeoutError:
                    print(f"L'analisi del pacchetto {package} ha superato il timeout di 60 minuti.")

                completed_packages += 1
                self.progress_signal.emit(int(completed_packages / total_packages * 100))

                if self.stopped:
                    break

            if not self.stopped:
                self.completed_signal.emit(
                    self.analysis_result.get_global_security_score(),
                    self.analysis_result.get_severity_count(),
                    self.analysis_result.get_vulnerabilities_list(),
                    self.analysis_result.get_package_detail())
            
    def process_package(self, file):
        if self.stopped:
            return

        package_name = f"{os.path.splitext(os.path.basename(file))[0]}"

        try:
            upload = self.upload_file(file)
            if "status" not in upload or upload["status"] != "success":
                raise AnalyzerError(f"Errore durante l'upload. Dettagli: {upload}")

            upload_hash = upload["hash"]

            scan = self.scan_file(file, upload_hash)
            if "error" in scan:
                raise AnalyzerError(f"Errore durante la scansione. Dettagli: {scan['error']}")

            security_score = self.get_security_score(upload_hash)
            json_report = self.generate_report_json(upload_hash)

            if security_score is not None and json_report is not None:
                pdf_name = os.path.join(utils.SCAN_RESULT_FOLDER, f"{package_name}.pdf")
                
                self.generate_report_pdf(upload_hash, pdf_name)
                self.analysis_result.append_result(package_name, security_score, json_report)

                self.delete_scan(upload_hash)
            else:
                print("La chiave 'security_score' non è presente nel risultato.")

        except Exception as e:
            print(e)
            error_message = f"Errore durante l'analisi del pacchetto {package_name}: {str(e)}"
            
            if "Connection refused" in str(e):
                error_message += "\nAssicurati che il server sia in esecuzione e che la connessione sia disponibile."
            elif "Max retries exceeded" in str(e):
                error_message += "\nVerifica che l'URL del server sia corretto e che il server sia raggiungibile."
                