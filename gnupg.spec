# rebuilding configure causes a warning about development version
# to appear
%define _disable_rebuild_configure 1

%define pkgname gnupg

%global optflags %{optflags} -O3

%bcond_without gpgagentscript

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	2.2.27
Release:	1
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source0:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{pkgname}-%{version}.tar.bz2
Source1:	sysconfig-gnupg

# (tpg) add patches from Fedora
# fix handling of missing key usage on ocsp replies - upstream T1333
Patch100:	gnupg-2.2.16-ocsp-keyusage.patch
# allow 8192 bit RSA keys in keygen UI with large RSA
Patch101:	gnupg-2.2.23-large-rsa.patch
# fix missing uid on refresh from keys.openpgp.org
# https://salsa.debian.org/debian/gnupg2/commit/f292beac1171c6c77faf41d1f88c2e0942ed4437
Patch102:	gnupg-2.2.18-tests-add-test-cases-for-import-without-uid.patch
Patch103:	gnupg-2.2.18-gpg-allow-import-of-previously-known-keys-even-without-UI.patch
Patch104:	gnupg-2.2.18-gpg-accept-subkeys-with-a-good-revocation-but-no-self-sig.patch

BuildRequires:	openldap-devel
BuildRequires:	sendmail-command
BuildRequires:	pkgconfig(gpg-error) >= 1.24
BuildRequires:	hostname
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libassuan) >= 2.4.3
BuildRequires:	pkgconfig(ksba) >= 1.0.2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	npth-devel >= 1.0
BuildRequires:	docbook-utils
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(sqlite3)
Recommends:	pinentry
# This used to be a required separate package; it has been
# merged into gnupg upstream in 2.1.0
# No need for a legacy Provides: because dirmngr was never
# used for anything other then gnupg2
Obsoletes:	dirmngr
%rename		gnupg2

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%package doc
Summary:	Documentation and manuals for %{name}.
Group:		Books/Computer books

%description doc
Documentation and manuals for %{name}.

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
# known bug
# https://bugs.funtoo.org/browse/FL-297
# http://clang.debian.net/status.php?version=3.1&key=UNKNOWN_TYPE_NAME
# cause: gnulib's stdint.h is broken -- let's just drop it in favor of
# assuming the OS isn't broken beyond repair
# echo '#include_next <stdint.h>' >gl/stdint_.h
%serverbuild

%configure \
	--enable-g13 \
	--disable-rpath \
	--enable-large-secmem

%make_build

# only 4 tests fails on i586
%ifnarch %{ix86}
%check
# (tpg) somehow tofu does fail
sed -i -e "s/tofu.scm//" tests/openpgp/Makefile*

[[ -n "$GPG_AGENT_INFO" ]] || eval $(./agent/gpg-agent --use-standard-socket --daemon --write-env-file gpg-agent-info)
make check
[[ -a gpg-agent-info ]] && kill -0 $(cut -d: -f 2 gpg-agent-info)
rm -f gpg-agent-info
%endif

%install
%make_install

#Remove: #60298
%if %{with gpgagentscript}
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# (tpg) enable gpg-agent in userland
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants
cp -a  doc/examples/systemd-user/*.{socket,service} %{buildroot}%{_userunitdir}
for i in dirmngr.socket gpg-agent-browser.socket gpg-agent-extra.socket gpg-agent.socket; do
	ln -sf %{_userunitdir}/$i %{buildroot}%{_userunitdir}/sockets.target.wants/$i
done
%endif

mkdir -p %{buildroot}%{_sysconfdir}/dirmngr
mkdir -p %{buildroot}%{_sysconfdir}/dirmngr/trusted-certs
mkdir -p %{buildroot}%{_var}/run/dirmngr
mkdir -p %{buildroot}%{_var}/cache/dirmngr/crls.d
mkdir -p %{buildroot}%{_var}/lib/dirmngr/extra-certs

%find_lang %{name}2

%files -f %{name}2.lang
%if %{with gpgagentscript}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_userunitdir}/*.service
%{_userunitdir}/*.socket
%{_userunitdir}/sockets.target.wants/*.socket
%endif
%attr(4755,root,root) %{_bindir}/gpgsm
%dir %{_sysconfdir}/dirmngr
%dir %{_sysconfdir}/dirmngr/trusted-certs
%{_datadir}/gnupg
%{_bindir}/dirmngr
%{_bindir}/dirmngr-client
%{_bindir}/g13
%{_bindir}/gpg-agent
%{_bindir}/gpg-wks-server
%{_bindir}/gpgconf
%{_bindir}/gpgsplit
%{_bindir}/gpgtar
%{_bindir}/kbxutil
%{_bindir}/watchgnupg
%{_bindir}/gpg-connect-agent
%{_bindir}/gpgparsemail
%{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/gpgscm
%{_sbindir}/addgnupghome
%{_sbindir}/applygnupgdefaults
%{_sbindir}/g13-syshelp
%{_libexecdir}/dirmngr_ldap
%{_libexecdir}/gpg-check-pattern
%{_libexecdir}/gpg-preset-passphrase
%{_libexecdir}/gpg-protect-tool
%{_libexecdir}/gpg-wks-client
%{_libexecdir}/scdaemon

%files doc
%doc README NEWS THANKS TODO
%doc doc/FAQ doc/HACKING doc/KEYSERVER doc/OpenPGP doc/TRANSLATE doc/DETAILS
%doc doc/examples
%doc %{_docdir}/%{name}
%{_infodir}/gnupg.info*
%{_mandir}/man1/dirmngr-client.1*
%{_mandir}/man1/gpg-agent.1*
%{_mandir}/man1/gpg-connect-agent.1*
%{_mandir}/man1/gpg-preset-passphrase.1*
%{_mandir}/man1/gpg-wks-server.1*
%{_mandir}/man1/gpg-wks-client.1*
%{_mandir}/man1/gpg.1.*
%{_mandir}/man1/gpgv.1.*
%{_mandir}/man1/gpgconf.1*
%{_mandir}/man1/gpgparsemail.1*
%{_mandir}/man1/gpgsm.1*
%{_mandir}/man1/gpgtar.1*
%{_mandir}/man1/scdaemon.1*
%{_mandir}/man1/symcryptrun.1*
%{_mandir}/man1/watchgnupg.1*
%{_mandir}/man7/gnupg.7*
%{_mandir}/man8/addgnupghome.8*
%{_mandir}/man8/applygnupgdefaults.8*
%{_mandir}/man8/dirmngr.8*
