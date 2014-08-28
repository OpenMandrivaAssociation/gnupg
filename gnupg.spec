%define	pkgname	gnupg

%bcond_without gpgagentscript

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	2.0.26
Release:	1
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source0:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{pkgname}-%{version}.tar.bz2
Source2:	gpg-agent.sh
Source3:	gpg-agent-xinit.sh
Source4:	sysconfig-gnupg
Patch0:		gnupg-1.9.3-use-ImageMagick-for-photo.patch
Patch1:		gnupg-2.0.20-tests-s2kcount.patch
BuildRequires:	openldap-devel
BuildRequires:	sendmail-command
BuildRequires:	libgpg-error-devel >= 1.4
BuildRequires:	libgcrypt-devel >= 1.2.0
BuildRequires:	libassuan-devel >= 1.0.2
BuildRequires:	libksba-devel >= 1.0.2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	docbook-utils
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	bzip2-devel
BuildRequires:	libassuan-devel
Requires:	dirmngr
Requires:	pinentry
%rename gnupg2

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .ImageMagick~
%patch1 -p1 -b .test~

%build
# known bug
# https://bugs.funtoo.org/browse/FL-297
# http://clang.debian.net/status.php?version=3.1&key=UNKNOWN_TYPE_NAME
export CC=gcc
%serverbuild

./autogen.sh

%configure \
	--enable-symcryptrun \
	--disable-rpath \
	--with-adns=no \
	--with-pkits-tests

# no parallel make (v2.0.5 at least)
%make

# all tests must pass on i586 and x86_64
%check
[[ -n "$GPG_AGENT_INFO" ]] || eval `./agent/gpg-agent --use-standard-socket --daemon --write-env-file gpg-agent-info`
make check
[[ -a gpg-agent-info ]] && kill -0 `cut -d: -f 2 gpg-agent-info`
rm -f gpg-agent-info

%install
%makeinstall_std
#Remove: #60298
%if %{with gpgagentscript}
install -d %{buildroot}/%{_sysconfdir}/profile.d
install %{SOURCE2} %{buildroot}/%{_sysconfdir}/profile.d/gpg-agent.sh
install -d %{buildroot}/%{_sysconfdir}/X11/xinit.d
install %{SOURCE3} %{buildroot}/%{_sysconfdir}/X11/xinit.d/gpg-agent
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%endif

ln -s gpg2 %{buildroot}%{_bindir}/gpg
ln -s gpgv2 %{buildroot}%{_bindir}/gpgv

%find_lang %{name}2

%files -f %{name}2.lang
%defattr(-,root,root)
%doc README NEWS THANKS TODO ChangeLog
%doc doc/FAQ doc/HACKING doc/KEYSERVER doc/OpenPGP doc/TRANSLATE doc/DETAILS 
%doc doc/examples
%if %{with gpgagentscript}
%attr(0755,root,root) %{_sysconfdir}/profile.d/gpg-agent.sh
%attr(0755,root,root) %{_sysconfdir}/X11/xinit.d/gpg-agent
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%attr(4755,root,root) %{_bindir}/gpgsm
%{_datadir}/gnupg
%{_bindir}/gpg-agent
%{_bindir}/gpgconf
%{_bindir}/kbxutil
%{_bindir}/watchgnupg
%{_bindir}/gpgsm-gencert.sh
%{_bindir}/gpgkey2ssh
%{_bindir}/gpg-connect-agent
%{_bindir}/gpgparsemail
%{_bindir}/gpg
%{_bindir}/gpg2
%{_bindir}/gpgv
%{_bindir}/gpgv2
%{_bindir}/symcryptrun
%{_sbindir}/addgnupghome
%{_sbindir}/applygnupgdefaults
%{_libexecdir}/gpg-check-pattern
%{_libexecdir}/gpg-preset-passphrase
%{_libexecdir}/gpg-protect-tool
%{_libexecdir}/gnupg-pcsc-wrapper
%{_libexecdir}/gpg2keys_curl
%{_libexecdir}/gpg2keys_finger
%{_libexecdir}/gpg2keys_hkp
%{_libexecdir}/gpg2keys_ldap
%{_libexecdir}/scdaemon
%{_infodir}/gnupg.info*
%{_mandir}/man1/gpg-agent.1*
%{_mandir}/man1/gpg-connect-agent.1*
%{_mandir}/man1/gpg-preset-passphrase.1*
%{_mandir}/man1/gpg2.1*
%{_mandir}/man1/gpgconf.1*
%{_mandir}/man1/gpgparsemail.1*
%{_mandir}/man1/gpgsm-gencert.sh.1*
%{_mandir}/man1/gpgsm.1*
%{_mandir}/man1/gpgv2.1*
%{_mandir}/man1/gpg-zip.1*
%{_mandir}/man1/scdaemon.1*
%{_mandir}/man1/symcryptrun.1*
%{_mandir}/man1/watchgnupg.1*
%{_mandir}/man8/addgnupghome.8*
%{_mandir}/man8/applygnupgdefaults.8*
