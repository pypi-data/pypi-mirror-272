from invoke import Program
from faasmsctl.tasks import task_ns
from faasmsctl.util.version import get_version


def main():
    program = Program(
        name="faasmsctl",
        binary="faasmsctl",
        binary_names=["faasmsctl"],
        namespace=task_ns,
        version=get_version(),
    )
    program.run()
