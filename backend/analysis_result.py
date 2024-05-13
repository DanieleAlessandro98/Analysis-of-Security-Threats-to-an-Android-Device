import json

class AnalysisResult:
    def __init__(self):
        self.security_score = []
        self.result_dict = {}
        self.package_dict = {}

    def append_result(self, package_name, security_score, json_report):
        self.package_dict[package_name] = security_score
        self.security_score.append(security_score)

        current_result_dict = self.extract_metadata_result(json_report)
        for key, value in current_result_dict.items():
            if (package_name, key) not in self.result_dict:
                self.result_dict[(package_name, key)] = value

    def extract_metadata_result(self, json_report):
        metadata_dict = {}
        code_analysis = json_report.get('code_analysis', {})
        findings = code_analysis.get('findings', {})

        for key, value in findings.items():
            if 'metadata' in value:
                metadata = value['metadata']
                metadata_dict[key] = {
                    'owasp-mobile': metadata.get('owasp-mobile'),
                    'masvs': metadata.get('masvs'),
                    'ref': metadata.get('ref'),
                    'severity': metadata.get('severity')
                }

        return metadata_dict

    def get_global_security_score(self):
        if len(self.security_score) == 0:
            return 0
        else:
            return sum(self.security_score) / len(self.security_score)

    def get_severity_count(self):
        severity_count_by_package = {}

        for (package_name, _), metadata in self.result_dict.items():
            severity_count = {"high": 0, "warning": 0, "info": 0, "secure": 0}

            severity = metadata["severity"]
            if severity == "high":
                severity_count["high"] += 1
            elif severity == "warning":
                severity_count["warning"] += 1
            elif severity == "info":
                severity_count["info"] += 1
            else:
                severity_count["secure"] += 1

            if package_name in severity_count_by_package:
                severity_count_by_package[package_name].update(severity_count)
            else:
                severity_count_by_package[package_name] = severity_count

        return severity_count_by_package

    def get_vulnerabilities_list(self):
        vulnerabilities_list = []
        for title, metadata in self.result_dict.items():
            vulnerability = {
                "title": title,
                "owasp-mobile": metadata.get('owasp-mobile', ''),
                "masvs": metadata.get('masvs', ''),
                "ref": metadata.get('ref', ''),
            }
            vulnerabilities_list.append(vulnerability)

        return vulnerabilities_list

    def get_package_detail(self):
        return self.package_dict
