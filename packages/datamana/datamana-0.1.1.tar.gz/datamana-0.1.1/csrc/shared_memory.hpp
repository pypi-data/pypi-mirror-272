#include <sys/mman.h>
#include <nanobind/nanobind.h>

namespace nb = nanobind;

struct SharedMemory {
    int fd;

    SharedMemory() : fd(-1) {}

    int py_shm_open(const char *name, int oflag, unsigned int mode) {
        int ret = shm_open(name, oflag, (mode_t)mode);
        if (ret == -1) {
            ret = errno;
        } else {
            fd = ret;
            ret = 0;
        }
        return ret;
    }
    int py_shm_unlink(const char *name) {
        int ret = shm_unlink(name);
        if (ret == -1)
            ret = errno;
        return ret;
    }
    int py_ftruncate(int length) {
        int ret = ftruncate(fd, (off_t)length);
        if (ret == -1)
            ret = errno;
        return ret;
    }
    int py_fchmod(unsigned int mode) {
        int ret = fchmod(fd, (mode_t)mode);
        if (ret == -1)
            ret = errno;
        return ret;
    }
};

void DEFINE_SHAREDMEMORY_MODULE(nb::module_ & (m)) {
    nb::class_<SharedMemory>(m, "SharedMemory")
        .def(nb::init<>())
        .def("open", &SharedMemory::py_shm_open)
        .def("unlink", &SharedMemory::py_shm_unlink)
        .def("ftruncate", &SharedMemory::py_ftruncate)
        .def("fchmod", &SharedMemory::py_fchmod)
        .def_prop_ro("fd", [](SharedMemory &shm) { return shm.fd; });
}
