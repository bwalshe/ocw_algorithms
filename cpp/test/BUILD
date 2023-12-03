load("@com_grail_bazel_compdb//:defs.bzl", "compilation_database")
load("@com_grail_bazel_output_base_util//:defs.bzl", "OUTPUT_BASE")

compilation_database(
    name = "test_compdb",
    targets = [
	":test_graph"
    ],
    # OUTPUT_BASE is a dynamic value that will vary for each user workspac
    # If you would like your build outputs to be the same across users, then
    # skip supplying this value, and substitute the default constant value
    # "__OUTPUT_BASE__" through an external tool like `sed` or `jq` (see
    # below shell commands for usage).
    output_base = OUTPUT_BASE,
    testonly=True,
)


cc_test(
	name = "test_graph",
	size = "small",
	srcs = ["test_graph.cpp"],
	deps = [
	    "//include:graph",
	    "@com_google_googletest//:gtest_main"
	],
)


cc_test(
	name = "test_circular",
	size = "small",
	srcs = ["test_circular.cpp"],
	deps = [
	    "//include:circular_list",
	    "@com_google_googletest//:gtest_main"
	],
)

cc_test(
    name = "test_fib",
    size = "small",
    srcs = ["test_fib.cpp"],
    deps = [
	"//include:fibheap",
	"@com_google_googletest//:gtest_main"
    ],
    copts = ["-g"],
)
