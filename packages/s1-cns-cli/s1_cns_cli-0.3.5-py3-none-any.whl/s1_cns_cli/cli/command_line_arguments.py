import argparse
from s1_cns_cli.cli.registry import OutputFormat, DEFAULT_SENTINELONE_CNS_DIR, GLOBAL_EPILOG, SCAN_EPILOG, CONFIG_EPILOG, \
    IAC_EPILOG, SECRET_EPILOG, VULN_EPILOG, SUPPORTED_GIT_PROVIDERS, DefaultGlobalConfigurations
from s1_cns_cli.cli.utils import get_home_path
from s1_cns_cli.version import build_type, version

APP_URL = "http://localhost:8080" if build_type == "local" else "https://app.pingsafe.com"


def evaluate_command_line_arguments():
    # Initialize global parser
    parser = argparse.ArgumentParser(
        prog='SentinelOneCnsCli',
        description='SentinelOne CNS CLI to scan code for vulnerabilities.',
        epilog=GLOBAL_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    add_global_flags(parser)
    scan_sub_parser, config_sub_parser = add_global_sub_parser(parser)

    # Initialized subparser for code parser
    iac_parser, secret_parser, vulnerability_parser = add_scan_sub_parser(scan_sub_parser)

    # s1-cns-cli code iac ...
    add_iac_flags(iac_parser)

    # s1-cns-cli code secret ...
    add_secret_flags(secret_parser)

    # s1-cns-cli code vuln ...
    add_vulnerability_flags(vulnerability_parser)

    # s1-cns-cli config ...
    add_config_global_flags(config_sub_parser)

    return parser.parse_args()


def add_global_flags(parser):
    # s1-cns-cli --all-sub-flags... (global flags)
    parser.add_argument("--disable-sentry", dest="disable_sentry", default=False, action="store_true",
                        help="disable sentry monitoring")
    parser.add_argument("--output-file", dest="global_output_file", metavar="", default="",
                        help="output file path")
    parser.add_argument("--output-format", dest="global_output_format", metavar="",
                        help="output format", choices=[OutputFormat.JSON, OutputFormat.CSV, OutputFormat.SARIF])
    parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", default=False,
                        help="show limited information")
    parser.add_argument("--verbose", dest="verbose", action="store_true", default=False,
                        help="show more information")
    parser.add_argument("-v", "--version", action="version", help="s1-cns-cli version",
                        version=version)
    parser.add_argument("--workers-count", dest="global_workers_count", metavar="",
                        help="worker count for concurrency")


def add_iac_flags(iac_parser):
    iac_parser.add_argument("--branch", dest="branch", help="specify current branch", metavar="", default="",
                            required=False)
    iac_parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="switch to debug mode")
    iac_parser.add_argument("-d", "--directory", dest="directory", default="", metavar="", help="directory to scan")
    iac_parser.add_argument("--download-external-modules", dest="download_external_modules", action="store_true",
                            default=True, help="download external modules used in code to scan")
    iac_parser.add_argument("--frameworks", dest="frameworks", nargs='+', default=["all"],
                            choices=["all", "terraform", "cloudformation", "kubernetes", "helm"],
                            metavar="",
                            help="IaC frameworks. Supported frameworks: [all, terraform, cloudformation, kubernetes, helm]")
    iac_parser.add_argument("--generate-baseline", dest="generate_baseline", action="store_true", default=False,
                            help="generate baseline to ignore issues")
    iac_parser.add_argument("--include-ignored", dest="include_ignored", action="store_true", default=False,
                            help="include ignored resources from baseline and exception management")
    iac_parser.add_argument("--invalidate-cache", dest="invalidate_cache", action="store_true", default=False,
                            help="delete all stored iac cache")
    iac_parser.add_argument("--list-plugins", dest="list_plugins", action="store_true", default=False,
                            help="list all plugins")
    iac_parser.add_argument("--output-file", dest="local_output_file", metavar="", default="",
                            help="output file path")
    iac_parser.add_argument("--output-format", dest="local_output_format", metavar="",
                            help="output format", choices=[OutputFormat.JSON, OutputFormat.CSV, OutputFormat.SARIF])
    iac_parser.add_argument("--pre-commit", dest="pre_commit", action="store_true", default=False,
                            help="scan pre-commit changes")
    iac_parser.add_argument("--publish-result", dest="publish_result", action="store_true",
                            default=False, help="publish scan results to SentinelOne CNS")
    iac_parser.add_argument("--repo-full-name", dest="repo_full_name",
                            help="specify repository full name(owner/repoName)", metavar="", default="",
                            required=False)
    iac_parser.add_argument("--repo-url", dest="repo_url",
                            help=f"specify repository full url. Supported providers: {', '.join(SUPPORTED_GIT_PROVIDERS)}",
                            metavar="", default="", required=False)
    iac_parser.add_argument("--skip-paths", dest="skip_paths", nargs="+", default=[], metavar="",
                            help="paths to be ignored during scan using a glob expression")
    iac_parser.add_argument("--var-file", dest="var_file", nargs="+", default=[], metavar="",
                            help="variables file path")


def add_secret_flags(secret_parser):
    secret_parser.add_argument("--all-commits", dest="all_commits", action="store_true", default=False,
                               help="scan entire commit history")
    secret_parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="switch to debug mode")
    secret_parser.add_argument("-d", "--directory", dest="directory", help="directory to scan", metavar="", default="",
                               required=False)
    secret_parser.add_argument("--disable-verification", dest="disable_verification", action="store_true",
                               default=False, help="disable verification of detected secrets")
    secret_parser.add_argument("--exclude-detectors", dest="exclude_detectors", metavar="", nargs="+", default=[],
                               help="detectors to be ignored during scan")
    secret_parser.add_argument("--exclude-extensions", dest="exclude_extensions", metavar="", nargs="+", default=[],
                               help="file extensions to be ignored during scan")
    secret_parser.add_argument("--generate-baseline", dest="generate_baseline", action="store_true", default=False,
                               help="generate baseline to ignore issues (available only for range scan)")
    secret_parser.add_argument("--include-ignored", dest="include_ignored", action="store_true", default=False,
                               help="include ignored secrets from baseline")
    secret_parser.add_argument("--list-detectors", dest="list_detectors", action="store_true", default=False,
                               help="list of all supported detectors")
    secret_parser.add_argument("--mask-secret", dest="mask_secret", action="store_true", default=False,
                               help="mask secret in output")
    secret_parser.add_argument("--output-file", dest="local_output_file", metavar="", default="",
                               help="output file path")
    secret_parser.add_argument("--output-format", dest="local_output_format", metavar="",
                               help="output format", choices=[OutputFormat.JSON, OutputFormat.CSV, OutputFormat.SARIF])
    secret_parser.add_argument("--pre-commit", dest="pre_commit", action="store_true", default=False,
                               help="scan pre-commit changes")
    secret_parser.add_argument("--publish-result", dest="publish_result", action="store_true", default=False,
                               help="publish scan results to SentinelOne CNS(works only with --pull-request and --pre-commit)")
    secret_parser.add_argument("--pull-request", dest="pull_request", nargs=2, type=str, metavar="", default=[],
                               help="scan pull request <src_branch dest_branch>")
    secret_parser.add_argument("--range", dest="range", nargs=2, type=str, metavar="", default=[],
                               help="scan range of commits <start-ref end-ref>")
    secret_parser.add_argument("--repo-full-name", dest="repo_full_name",
                               help="specify repository full name (owner/repositoryName)", metavar="",
                               default="", required=False)
    secret_parser.add_argument("--repo-url", dest="repo_url",
                               help=f"specify repository full url. Supported providers: {', '.join(SUPPORTED_GIT_PROVIDERS)}",
                               metavar="", default="", required=False)
    secret_parser.add_argument("--skip-paths", dest="skip_paths", nargs="+", default=[], metavar="",
                               help="paths to be ignored during scan using a glob expression")
    secret_parser.add_argument("--scan-commit", dest="scan_commit", type=str, const="", nargs="?", metavar="",
                               help="scan a particular commit (default: head)")
    secret_parser.add_argument("--verified-only", dest="verified_only", action="store_true", default=False,
                               help="give results for verified secrets only")


def add_vulnerability_flags(vulnerability_parser):
    vulnerability_parser.add_argument("--debug", dest="debug", action="store_true", default=False,
                                      help="switch to debug mode")
    vulnerability_parser.add_argument("-d", "--directory", dest="directory", metavar="", default="",
                                      help="directory to scan for vulnerabilities")
    vulnerability_parser.add_argument("--docker-image", dest="docker_image", metavar="", default="",
                                      help="docker image to scan for vulnerabilities")
    vulnerability_parser.add_argument("--fixed-only", dest="only_fixed", action="store_true", default=False,
                                      help="ignore vulnerabilities for which fix/patch is not available yet!")
    vulnerability_parser.add_argument("--generate-sbom", dest="generate_sbom", action="store_true", default=False,
                                      help="generate SBOM(software bill of materials)")
    vulnerability_parser.add_argument("--output-file", dest="local_output_file", metavar="", default="",
                                      help="output file path")
    vulnerability_parser.add_argument("--output-format", dest="local_output_format", metavar="",
                                      help="output format",
                                      choices=[OutputFormat.JSON, OutputFormat.CSV, OutputFormat.SARIF])
    vulnerability_parser.add_argument("--password", dest="password", metavar="", default="",
                                      help="specify password/auth-token for registry")
    vulnerability_parser.add_argument("--platform", dest="platform", metavar="", default="linux/arm64",
                                      help="specify image platform (default: linux/arm64)")
    vulnerability_parser.add_argument("--registry", dest="registry", metavar="", default="index.docker.io",
                                      help="specify registry for image (default: index.docker.io)")
    vulnerability_parser.add_argument("--sbom-format", dest="sbom_format", metavar="",
                                      choices=["s1-cns-json", "cyclonedx-json", "spdx-json"],
                                      help="sbom output format, options=[s1-cns-json, cyclonedx-json, spdx-json] ("
                                           "default=s1-cns-json)")
    vulnerability_parser.add_argument("--skip-paths", dest="skip_paths", nargs="+", default=[], metavar="",
                                      help="paths to be ignored during scan using a glob expression")
    vulnerability_parser.add_argument("--username", dest="username", metavar="", default="",
                                      help="specify username for registry")
    vulnerability_parser.add_argument("--vuln-format", dest="vuln_format", default="s1-cns-json", metavar="",
                                      choices=["s1-cns-json", "defect-dojo-generic-format"],
                                      help="vulnerability scan export format, options=[s1-cns-json, "
                                           "defect-dojo-generic-format] ("
                                           "default=sentinelone-json)")


def add_config_global_flags(config_sub_parser):
    config_sub_parser.add_argument("--api-token", dest="api_token", required=False, default="",
                                   help="api-token for s1-cns-cli")
    config_sub_parser.add_argument("--cache-directory", dest="cache_directory", metavar="",
                                   default=get_home_path(DEFAULT_SENTINELONE_CNS_DIR),
                                   help=f"s1-cns-cli cache dir (default='{get_home_path(DEFAULT_SENTINELONE_CNS_DIR)}')")
    config_sub_parser.add_argument("--debug", dest="debug", action="store_true", default=False,
                                   help="debug config command")
    config_sub_parser.add_argument("--output-format", dest="output_format", metavar="",
                                   help="output format for results",
                                   default=DefaultGlobalConfigurations.OUTPUT_FORMAT.value,
                                   choices=[OutputFormat.JSON, OutputFormat.CSV])
    config_sub_parser.add_argument("--output-file", dest="output_file", metavar="", default="",
                                   help="output file location")
    config_sub_parser.add_argument("--workers-count", dest="workers_count",
                                   default=DefaultGlobalConfigurations.WORKERS_COUNT.value, metavar="",
                                   help="worker count for concurrency")
    config_sub_parser.add_argument("--endpoint-url", dest="endpoint_url", default=APP_URL, metavar="",
                                   help="SentinelOne CNS Endpoint URL")
    config_sub_parser.add_argument("--on-crash-exit-code", dest="on_crash_exit_code",
                                   default=DefaultGlobalConfigurations.ON_CRASH_EXIT_CODE.value,
                                   metavar="", type=int,
                                   help="Exit status when something went wrong")


def add_global_sub_parser(parser):
    # Initialized subparser for global parser
    sub_parser = parser.add_subparsers(dest="main_sub_parser", title="Sub Commands",
                                       description="Use following sub-commands to configure SentinelOne CNS CLI or scan your code.",
                                       help="Description")

    # s1-cns-cli subcommand[scan/config]
    scan_sub_parser = sub_parser.add_parser("scan",
                                            prog="Code Scanner",
                                            description="SentinelOne CNS CLI scan sub-command allows three types of scan(iac, secret and vuln)",
                                            help="code scanner",
                                            epilog=SCAN_EPILOG,
                                            formatter_class=argparse.RawDescriptionHelpFormatter
                                            )
    config_sub_parser = sub_parser.add_parser("config",
                                              prog="Configure SentinelOne CNS CLI",
                                              description="Configure your SentinelOne CNS CLI",
                                              help="configure SentinelOne CNS cli",
                                              epilog=CONFIG_EPILOG,
                                              formatter_class=argparse.RawDescriptionHelpFormatter
                                              )

    return scan_sub_parser, config_sub_parser


def add_scan_sub_parser(scan_sub_parser):
    sub_parser = scan_sub_parser.add_subparsers(dest="scan_type_sub_parser", help="Scan Type")
    iac_parser = sub_parser.add_parser("iac",
                                       prog="IaC",
                                       description="SentinelOne CNS CLI detects misconfigurations in your IaC repository.",
                                       help="Infrastructure as a Code Scanning",
                                       epilog=IAC_EPILOG,
                                       formatter_class=argparse.RawDescriptionHelpFormatter
                                       )
    secret_parser = sub_parser.add_parser("secret",
                                          prog="Secret Detection",
                                          description="SentinelOne CNS CLI detects secrets present in your repository.",
                                          help="Secret Detection",
                                          epilog=SECRET_EPILOG,
                                          formatter_class=argparse.RawDescriptionHelpFormatter
                                          )
    vulnerability_parser = sub_parser.add_parser("vuln",
                                                 prog="Vulnerability Scanner and SBOM generator",
                                                 description="SentinelOne CNS CLI detects vulnerable dependencies and generates SBOM used in your repository/image.",
                                                 help="Vulnerability Scanner and SBOM generator",
                                                 epilog=VULN_EPILOG,
                                                 formatter_class=argparse.RawDescriptionHelpFormatter
                                                 )
    return iac_parser, secret_parser, vulnerability_parser
