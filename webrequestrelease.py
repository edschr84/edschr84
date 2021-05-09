from bs4 import BeautifulSoup
import requests
import re
import os

build_dir = "/root/docker_image/"
if not os.path.exists(build_dir):  
    os.mkdir(build_dir)

distro = ""
release_ver = ""
url = ""
packages = ""
package_path_list = []

def distro_release_version():
    global url, packages, release_ver, distro
    if distro == "1":
        print('What version of Centos?')
        release_ver = input("#!#")
        if release_ver == '8':
            url = 'http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/'
            packages = ["centos-linux-release", "centos-linux-repos", "centos-gpg-keys"]
            package_list()
        elif release_ver == '7':
            url = 'http://mirror.centos.org/centos/7/os/x86_64/Packages/'
            packages = ["centos-release"]
            package_list()
    if distro == "2":
        print('Which release of Fedora?:')
        release_ver = input('#1#')
        url = 'http://mirror.bytemark.co.uk/fedora/linux/releases/' + release_ver + '/Everything/x86_64/os/Packages/f/'
        package_list()
        packages = ["fedora-release-" + release_ver, "fedora-repos-" + release_ver, "fedora-gpg-keys"]


def package_list():
    global packages, url, package_path_list
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
        package_list = link.get('href')
        for package in packages:
            if re.match(package, package_list):
                full_url = ''.join([url, package_list])
                package_path = ''.join([build_dir, package_list])
                request = requests.get(full_url)
                package_path_list.append(package_path)
                open(package_path, 'wb').write(request.content)
                print(full_url, end="")
                print("---\/-## Fetched ##")


if __name__ == "__main__":

    print("Which Distribution image would you like to create?: 1 - CentOS; 2 - Fedora; 3 - Debian")
    distro = input("#!#")
    distro_release_version()
    print("The following packages were downloaded:")
    for package in package_path_list:
        print(package)

