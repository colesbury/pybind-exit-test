#include <pybind11/pybind11.h>
#include <unistd.h>

namespace py = pybind11;

void read_pipe_pybind(int fd) {
    py::gil_scoped_release release;

    // Some long running computation. We read from a pipe here
    // to reliably ensure that this "finishes" during the shutdown
    // process.
    char buf[128];
    ssize_t n = read(fd, &buf, sizeof(buf));
    (void)n;
}

void read_pipe_capi(int fd) {
    Py_BEGIN_ALLOW_THREADS
    // Some long running computation. We read from a pipe here
    // to reliably ensure that this "finishes" during the shutdown
    // process.
    char buf[128];
    ssize_t n = read(fd, &buf, sizeof(buf));
    (void)n;
    Py_END_ALLOW_THREADS
}

PYBIND11_MODULE(pybind_exit_test, m) {
    m.def("read_pipe_pybind", &read_pipe_pybind);
    m.def("read_pipe_capi", &read_pipe_capi);
}
