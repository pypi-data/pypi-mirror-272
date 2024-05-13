import tempfile
from inspect import FrameInfo
from pathlib import Path

from approvaltests import Reporter, StackFrameNamer
from approvaltests.inline.split_code import SplitCode


class InlinePythonReporter(Reporter):
    def __init__(self, reporter, add_approval_line=False):
        self.diffReporter = reporter
        self.semi_automatic_extra_line = (
            "\n***** DELETE ME TO APPROVE *****" if add_approval_line else ""
        )

    def report(self, received_path: str, approved_path: str) -> bool:
        test_source_file = self.get_test_source_file()
        received_path = self.create_received_file(received_path, test_source_file)
        return self.diffReporter.report(received_path, test_source_file)

    def get_test_source_file(self):
        test_stack_frame: FrameInfo = StackFrameNamer.get_test_frame()
        return test_stack_frame.filename

    def create_received_file(self, received_path: str, test_source_file: str):
        code = Path(test_source_file).read_text()
        received_text = (
            Path(received_path).read_text()[:-1] + self.semi_automatic_extra_line
        )
        method_name = StackFrameNamer.get_test_frame().function
        new_code = self.swap(received_text, code, method_name)
        file = tempfile.NamedTemporaryFile(suffix=".received.txt", delete=False).name
        Path(file).write_text(new_code)
        return file

    def swap(self, received_text, code, method_name):
        split_code = SplitCode.on_method(code, method_name)
        return f'{split_code.before_method}\n{split_code.tab}"""\n{split_code.indent(received_text)}\n{split_code.tab}"""\n{split_code.after_method}'
