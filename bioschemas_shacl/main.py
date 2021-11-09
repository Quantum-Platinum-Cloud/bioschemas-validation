import sys
import argparse
import logging
import time
from argparse import RawTextHelpFormatter
from rich.console import Console
from rich.table import Table
from tabulate import tabulate
from rich.text import Text

# from rich.progress import track

from bioschemas_profile_shape.WebResource import WebResource
from bioschemas_profile_shape.bioschemas_shape_gen import validate_any_from_microdata

parser = argparse.ArgumentParser(
    description="""
Bioschemas-shacl-validator, a command line tool to validate bisochemas annotated web resources.

Usage examples :
    python main.py --u https://bgee.org/?page=gene&gene_id=ENSG00000274928 

Please report any issue to thomas.rosnet@france-bioinforatique.fr, alban.gaignard@univ-nantes.fr
""",
    formatter_class=RawTextHelpFormatter,
)

parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    required=False,
    help="enables debugging logs",
    dest="debug",
)

parser.add_argument(
    "-u",
    "--urls",
    nargs="+",
    required=False,
    help="list of URLs to be tested",
    dest="urls",
)
# parser.add_argument(
#     "-bs",
#     "--bioschemas",
#     action="store_true",
#     required=False,
#     help="validate Bioschemas profiles",
#     dest="bioschemas",
# )


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        args = parser.parse_args()

        if args.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)-8s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        else:
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)-8s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        LOGGER = logging.getLogger()
        if not LOGGER.handlers:
            LOGGER.addHandler(logging.StreamHandler(sys.stdout))

        if args.urls:
            start_time = time.time()

            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Errors", justify="right")
            table.add_column("Warnings", justify="right")

            for url in args.urls:
                console.rule(f"[bold red]Bioschemas validation for URL {url}")
                res = validate_any_from_microdata(input_url=url)
                console.print(res)

                # print(tabulate({"Warnings": res[id]["warnings"],
                #                 "Errors": res[id]["warnings"]}, headers = "keys"))


                # print(res[url]["errors"])
                # print(res[url]["warnings"])

                # for m in track(metrics_collection, "Processing FAIR metrics ..."):
                #     logging.info(m.get_name())
                #     res = m.evaluate()
                #     if m.get_name().startswith("F"):
                #         table.add_row(
                #             Text(
                #                 m.get_name() + " " + str(res), style=get_result_style(res)
                #             ),
                #             "",
                #             "",
                #             "",
                #         )
                #     elif m.get_name().startswith("A"):
                #         table.add_row(
                #             "",
                #             Text(
                #                 m.get_name() + " " + str(res), style=get_result_style(res)
                #             ),
                #             "",
                #             "",
                #         )
                #     elif m.get_name().startswith("I"):
                #         table.add_row(
                #             "",
                #             "",
                #             Text(
                #                 m.get_name() + " " + str(res), style=get_result_style(res)
                #             ),
                #             "",
                #         )
                #     elif m.get_name().startswith("R"):
                #         table.add_row(
                #             "",
                #             "",
                #             "",
                #             Text(f"{m.get_name()} {str(res)}", style=get_result_style(res)),
                #         )

            console.rule(f"[bold red]Bioschemas validation for URL {url}")
            #console.print(table)
            elapsed_time = round((time.time() - start_time), 2)
            logging.info(f"Bioschemas validation processed in {elapsed_time} s")

    finally:
        WebResource.WEB_BROWSER_HEADLESS.quit()
