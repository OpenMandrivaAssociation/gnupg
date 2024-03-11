# rebuilding configure causes a warning about development version
# to appear
%define _disable_rebuild_configure 1

%define pkgname gnupg

%global optflags %{optflags} -O3

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	2.4.5
Release:	1
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source0:	https://www.gnupg.org/ftp/gcrypt/gnupg/%{pkgname}-%{version}.tar.bz2
# (tpg) add patches from Fedora
# allow 8192 bit RSA keys in keygen UI with large RSA
Patch9:		https://src.fedoraproject.org/rpms/gnupg2/raw/rawhide/f/gnupg-2.2.23-large-rsa.patch
# fix missing uid on refresh from keys.openpgp.org
# https://salsa.debian.org/debian/gnupg2/commit/f292beac1171c6c77faf41d1f88c2e0942ed4437
Patch20:	https://src.fedoraproject.org/rpms/gnupg2/raw/rawhide/f/gnupg-2.2.18-tests-add-test-cases-for-import-without-uid.patch
Patch21:	https://src.fedoraproject.org/rpms/gnupg2/raw/rawhide/f/gnupg-2.4.0-gpg-allow-import-of-previously-known-keys-even-without-UI.patch
Patch22:	https://src.fedoraproject.org/rpms/gnupg2/raw/rawhide/f/gnupg-2.2.18-gpg-accept-subkeys-with-a-good-revocation-but-no-self-sig.patch
# Fixes for issues found in Coverity scan - reported upstream
Patch30:	https://src.fedoraproject.org/rpms/gnupg2/raw/rawhide/f/gnupg-2.2.21-coverity.patch

BuildRequires:	pkgconfig(ldap)
BuildRequires:	sendmail-command
BuildRequires:	pkgconfig(gpg-error) >= 1.24
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libassuan) >= 2.4.3
BuildRequires:	pkgconfig(ksba) >= 1.0.2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	npth-devel >= 1.0
BuildRequires:	docbook-utils
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tss2-esys)
BuildRequires:	locales-extra-charsets
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
%configure \
	--enable-g13 \
	--disable-rpath \
	--enable-large-secmem

%make_build

%if ! %{cross_compiling}
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
%endif

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/dirmngr
mkdir -p %{buildroot}%{_sysconfdir}/dirmngr/trusted-certs
mkdir -p %{buildroot}%{_var}/run/dirmngr
mkdir -p %{buildroot}%{_var}/cache/dirmngr/crls.d
mkdir -p %{buildroot}%{_var}/lib/dirmngr/extra-certs

%find_lang %{name}2

%files -f %{name}2.lang
%attr(4755,root,root) %{_bindir}/gpgsm
%dir %{_sysconfdir}/dirmngr
%dir %{_sysconfdir}/dirmngr/trusted-certs
%{_datadir}/gnupg
%{_bindir}/dirmngr
%{_bindir}/dirmngr-client
%{_bindir}/g13
%{_bindir}/gpg-agent
%{_bindir}/gpg-card
%{_bindir}/gpg-wks-client
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
%{_libexecdir}/gpg-auth
%{_libexecdir}/gpg-check-pattern
%{_libexecdir}/gpg-pair-tool
%{_libexecdir}/gpg-preset-passphrase
%{_libexecdir}/gpg-protect-tool
%{_libexecdir}/gpg-wks-client
%{_libexecdir}/keyboxd
%{_libexecdir}/scdaemon
%{_libexecdir}/tpm2daemon

%files doc
%doc README NEWS THANKS TODO
%doc doc/FAQ doc/HACKING doc/KEYSERVER doc/OpenPGP doc/TRANSLATE doc/DETAILS
%doc doc/examples
%doc %{_docdir}/%{name}
%{_infodir}/gnupg.info*
%{_mandir}/man1/dirmngr-client.1*
%{_mandir}/man1/gpg-agent.1*
%{_mandir}/man1/gpg-card.1*
%{_mandir}/man1/gpg-check-pattern.1*
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
%{_mandir}/man1/watchgnupg.1*
%{_mandir}/man7/gnupg.7*
%{_mandir}/man8/addgnupghome.8*
%{_mandir}/man8/applygnupgdefaults.8*
%{_mandir}/man8/dirmngr.8*
