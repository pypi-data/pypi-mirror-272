from cowboy_lib.repo.source_repo import SourceRepo
from cowboy_lib.repo.repository import PatchFile, PatchFileContext
from cowboy_lib.coverage import TestCoverage
from cowboy_lib.repo.source_file import NodeType
from cowboy_lib.test_modules.test_module import TestModule

from logging import getLogger
import random
import sys
from pathlib import Path
from typing import List, Tuple
import os

logger = getLogger("test_results")


class TestInCoverageException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "Test files are included in coverage report"


def testfiles_in_coverage(base_cov: TestCoverage, src_repo: SourceRepo) -> bool:
    """
    Check if the test files are accidentally included in the coverage
    """
    for test_file in src_repo.test_files:
        for cov in base_cov.cov_list:
            if cov.filename.split(os.sep)[-1] == test_file.path.name:
                print(cov.filename.split(os.sep)[-1], test_file.path.name)

                return True
    return False


def get_tm_target_coverage(
    repo_ctxt: RepoTestContext,
    tm: TestModule,
    base_cov: TestCoverage,
) -> Tuple[List[TestModule], TestCoverage]:
    """
    Test augmenting existing test classes by deleting random test methods, and then
    having LLM strategy generate them. Coverage is taken:
    1. After the deletion
    2. After the deletion with newly generated LLM testcases

    The diff measures how well we are able to supplant the coverage of the deleted methods
    """

    if testfiles_in_coverage(base_cov, repo_ctxt.src_repo):
        raise TestInCoverageException

    # First loop we find the total coverage of each test by itself
    try:
        only_module = [tm.name]
        # coverage with ONLY the current test module turned on
        module_cov, *_ = repo_ctxt.runner.run_test(
            include_tests=only_module, cache=False
        )

        module_diff = base_cov - module_cov.coverage
        total_cov_diff = module_diff.total_cov.covered
        if total_cov_diff > 0:
            logger.info(f"{tm.name} completed with cov diff: {total_cov_diff}")

            # part 2:
            single_covs = []
            for test in tm.tests:
                # tm.test_file.delete(test.name, node_type=test.type)
                # deleted_file = PatchFile(tm.test_file.path, tm.test_file.to_code())
                # with PatchFileContext(repo_ctxt.git_repo, deleted_file):

                # exclude_test = get_exclude_path(test, tm.test_file.path)
                single_cov, *_ = repo_ctxt.runner.run_test(
                    exclude_tests=[(test, tm.test_file.path)],
                    include_tests=only_module,
                    cache=False,
                )

                print(
                    f"Module cov: {module_cov.coverage.total_cov.covered}, Single cov: {single_cov.coverage.total_cov.covered}"
                )

                single_diff = (module_cov.coverage - single_cov.coverage).cov_list
                for c in single_diff:
                    logger.info(
                        f"Changed coverage from deleting {test.name}:\n {c.__str__()}"
                    )

                # dont think we actually need this here .. confirm
                repo_ctxt.src_repo = SourceRepo(repo_ctxt.src_repo.repo_path)
                tm.test_file = repo_ctxt.src_repo.get_file(tm.test_file.path)
                single_covs.extend(single_diff)

            # re-init the chunks according to the aggregated individual test coverages
            tm.set_chunks(
                single_covs,
                source_repo=repo_ctxt.src_repo,
                base_path=repo_ctxt.repo_path,
            )

            logger.info(f"Chunks: \n{tm.print_chunks()}")
        # Find out what's the reason for the missed tests
        else:
            logger.info(f"No coverage difference found for {tm.name}")

    except Exception as e:
        logger.info(
            f"Exception on {tm.name} in {tm.test_file.path}",
            exc_info=True,
        )

    logger.info(f"Saved as {repo_ctxt.exp_id}")

    return tm


# def get_total_module_coverage(tms: List[TestModule], base_cov: TestCoverage):
#     """
#     Calculates how much of total coverage is actually covered by test modules

#     The score returned is lower (significantly) than the total coverage because it only
#     takes into account the the
#     """

#     def get_file_coverage(tms: List[TestModule], filename):
#         seen_chunks = []
#         covered_lines = 0
#         for tm in tms:
#             for chunk in tm.chunks:
#                 if str(chunk.base_path()) == filename:
#                     if chunk not in seen_chunks:
#                         seen_chunks.append(chunk)
#                         covered_lines += len(chunk.lines)
#         return covered_lines

#     total_tm = 0
#     total_base = 0
#     for cov in base_cov.cov_list:
#         covered_by_base = cov.stmts - cov.misses
#         covered_by_tm = get_file_coverage(tms, cov.filename)
#         # print(covered_by_tm, covered_by_base, cov.filename)
#         total_tm += covered_by_tm
#         total_base += covered_by_base

#     return total_tm, total_base
