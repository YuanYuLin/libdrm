import ops
import iopc

TARBALL_FILE="libdrm-2.4.91.tar.bz2"
TARBALL_DIR="libdrm-2.4.91"
INSTALL_DIR="libdrm-bin"
pkg_path = ""
output_dir = ""
tarball_pkg = ""
tarball_dir = ""
install_dir = ""
install_tmp_dir = ""
cc_host = ""
tmp_include_dir = ""
dst_include_dir = ""
dst_lib_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global tarball_pkg
    global install_dir
    global install_tmp_dir
    global tarball_dir
    global cc_host
    global tmp_include_dir
    global dst_include_dir
    global dst_lib_dir
    global dst_bin_dir
    global install_test_utils
    global src_pkgconfig_dir
    global dst_pkgconfig_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball_pkg = ops.path_join(pkg_path, TARBALL_FILE)
    install_dir = ops.path_join(output_dir, INSTALL_DIR)
    install_tmp_dir = ops.path_join(output_dir, INSTALL_DIR + "-tmp")
    tarball_dir = ops.path_join(output_dir, TARBALL_DIR)
    cc_host_str = ops.getEnv("CROSS_COMPILE")
    cc_host = cc_host_str[:len(cc_host_str) - 1]
    tmp_include_dir = ops.path_join(output_dir, ops.path_join("include",args["pkg_name"]))
    dst_include_dir = ops.path_join("include",args["pkg_name"])
    dst_lib_dir = ops.path_join(install_dir, "lib")
    dst_bin_dir = ops.path_join(install_dir, "bin")
    src_pkgconfig_dir = ops.path_join(pkg_path, "pkgconfig")
    dst_pkgconfig_dir = ops.path_join(install_dir, "pkgconfig")
    if ops.getEnv("INSTALL_TEST_UTILS") == 'y':
        install_test_utils = True
    else:
        install_test_utils = False

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("DESTDIR", install_tmp_dir))
    ops.exportEnv(ops.setEnv("SUPPORT_DRM", "y"))

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarBz2(tarball_pkg, output_dir)
    #ops.copyto(ops.path_join(pkg_path, "finit.conf"), output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(tarball_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    cflags = iopc.get_includes()
    libs = iopc.get_libs()

    extra_conf = []
    extra_conf.append("--host=" + cc_host)
    extra_conf.append("--enable-intel")
    extra_conf.append("--enable-radeon")
    extra_conf.append("--enable-amdgpu")
    extra_conf.append("--enable-nouveau")
    extra_conf.append("--enable-vmwgfx")
    extra_conf.append("--enable-freedreno")
    extra_conf.append("--enable-vc4")
    if install_test_utils:
        extra_conf.append("--enable-install-test-programs")

    extra_conf.append('FFI_CFLAGS=' + cflags)
    extra_conf.append('FFI_LIBS=' + libs)
    extra_conf.append('EXPAT_CFLAGS=' + cflags)
    extra_conf.append('EXPAT_LIBS=' + libs)
    extra_conf.append('LIBXML_CFLAGS=' + cflags)
    extra_conf.append('LIBXML_LIBS=' + libs)
    extra_conf.append('PCIACCESS_CFLAGS=' + cflags)
    extra_conf.append('PCIACCESS_LIBS=' + libs)
    iopc.configure(tarball_dir, extra_conf)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.mkdir(install_dir)
    ops.mkdir(install_tmp_dir)
    iopc.make(tarball_dir)
    iopc.make_install(tarball_dir)

    ops.mkdir(install_dir)
    ops.mkdir(dst_lib_dir)
    libdrm = "libdrm.so.2.4.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm, "libdrm.so.2.4")
    ops.ln(dst_lib_dir, libdrm, "libdrm.so.2")
    ops.ln(dst_lib_dir, libdrm, "libdrm.so")

    libkms = "libkms.so.1.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libkms), dst_lib_dir)
    ops.ln(dst_lib_dir, libkms, "libkms.so.1.0")
    ops.ln(dst_lib_dir, libkms, "libkms.so.1")
    ops.ln(dst_lib_dir, libkms, "libkms.so")

    libdrm_amdgpu = "libdrm_amdgpu.so.1.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm_amdgpu), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm_amdgpu, "libdrm_amdgpu.so.1.0")
    ops.ln(dst_lib_dir, libdrm_amdgpu, "libdrm_amdgpu.so.1")
    ops.ln(dst_lib_dir, libdrm_amdgpu, "libdrm_amdgpu.so")

    libdrm_freedreno = "libdrm_freedreno.so.1.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm_freedreno), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm_freedreno, "libdrm_freedreno.so.1.0")
    ops.ln(dst_lib_dir, libdrm_freedreno, "libdrm_freedreno.so.1")
    ops.ln(dst_lib_dir, libdrm_freedreno, "libdrm_freedreno.so")

    libdrm_intel = "libdrm_intel.so.1.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm_intel), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm_intel, "libdrm_intel.so.1.0")
    ops.ln(dst_lib_dir, libdrm_intel, "libdrm_intel.so.1")
    ops.ln(dst_lib_dir, libdrm_intel, "libdrm_intel.so")

    libdrm_nouveau = "libdrm_nouveau.so.2.0.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm_nouveau), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm_nouveau, "libdrm_nouveau.so.2.0")
    ops.ln(dst_lib_dir, libdrm_nouveau, "libdrm_nouveau.so.2")
    ops.ln(dst_lib_dir, libdrm_nouveau, "libdrm_nouveau.so")

    libdrm_radeon = "libdrm_radeon.so.1.0.1"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libdrm_radeon), dst_lib_dir)
    ops.ln(dst_lib_dir, libdrm_radeon, "libdrm_radeon.so.1.0")
    ops.ln(dst_lib_dir, libdrm_radeon, "libdrm_radeon.so.1")
    ops.ln(dst_lib_dir, libdrm_radeon, "libdrm_radeon.so")

    ops.mkdir(tmp_include_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/include/."), tmp_include_dir)

    ops.mkdir(dst_pkgconfig_dir)
    ops.copyto(ops.path_join(src_pkgconfig_dir, '.'), dst_pkgconfig_dir)

    if install_test_utils:
        ops.mkdir(dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/kms-steal-crtc"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/kmstest"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/kms-universal-planes"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/modeprint"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/modetest"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/proptest"), dst_bin_dir)
        ops.copyto(ops.path_join(install_tmp_dir, "usr/local/bin/vbltest"), dst_bin_dir)
    return True

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(ops.path_join(install_dir, "lib"), "."), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(tmp_include_dir, "."), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(dst_pkgconfig_dir, '.'), "pkgconfig")
    if install_test_utils:
        iopc.installBin(args["pkg_name"], ops.path_join(ops.path_join(install_dir, "bin"), "."), "bin")

    return False

def MAIN_SDKENV(args):
    set_global(args)

    pkgsdk_include_dir=ops.path_join(iopc.getSdkPath(), 'usr/include/' + args["pkg_name"])
    cflags = ""
    cflags += " -I" + pkgsdk_include_dir
    cflags += " -I" + ops.path_join(pkgsdk_include_dir, "libdrm")
    iopc.add_includes(cflags)

    libs = ""
    libs += " -ldrm -lkms -ldrm_amdgpu -ldrm_freedreno -ldrm_intel -ldrm_nouveau -ldrm_radeon"
    iopc.add_libs(libs)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

