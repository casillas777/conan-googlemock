from conans import ConanFile, CMake, tools
import os


class GooglemockConan(ConanFile):
    name = "googlemock"
    version = "1.8.0"
    url = "https://github.com/casillas777/conan-googlemock.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    _inner_folder_postfix = "release-%s" % version
    _inner_folder = "googletest-%s" % _inner_folder_postfix

    def source(self):
        download_filename = "%s.zip" % self._inner_folder_postfix
        tools.download('https://github.com/google/googletest/archive/%s' % download_filename, download_filename)
        tools.unzip(download_filename)
        os.unlink(download_filename)
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("%s/CMakeLists.txt" % self._inner_folder, "project( googletest-distribution )", '''project( googletest-distribution )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)

        if self.options.shared:
            cmake.definitions['BUILD_SHARED_LIBS'] = 'ON'

        if self.settings.compiler == 'Visual Studio':
            if (self.settings.compiler.runtime == 'MD') or (self.settings.compiler.runtime == 'MDd'):
                cmake.definitions['gtest_force_shared_crt'] = 'ON'
			
        cmake.configure(source_dir=os.path.join(self.conanfile_directory, self._inner_folder))
        cmake.build()
        #shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        
        #self.run('cmake %s %s %s' % (self._inner_folder, cmake.command_line, shared))
        #self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="%s/googlemock/include" % self._inner_folder)
        self.copy("*.h", dst="include", src="%s/googletest/include" % self._inner_folder)
		
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("*.dll", dst="lib", src="lib", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = [ "gmock", "gmock_main", "gtest", "gtest_main" ]
        if (self.settings.os == "Linux"):
            self.cpp_info.libs.append("pthread")

        self.cpp_info.libdirs = ["lib"]
