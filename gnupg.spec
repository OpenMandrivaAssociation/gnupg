%bcond_without	openldap

Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	1.4.13
Release:	4
License:	GPLv3
Group:		File tools
Url:		http://www.gnupg.org
Source0:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2.sig
Source2:	mdk-keys.tar.bz2
Source3:	mdk-keys.tar.bz2.sig
Patch1:		gnupg-1.4.2.2-use-agent-by-default.diff
Patch4:		gnupg-1.4.5-ppc64.patch
# splitted off from the previous debian patch
Patch6:		gnupg-1.4.7-deb-free_caps.patch
Patch7:		gnupg-1.4.7-deb-manpage.patch
Patch8:		gnupg-1.4.7-deb-min_privileges.patch

BuildRequires:	bison
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	postfix #sendmail-command
BuildRequires:	bzip2-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(ncursesw)
%if %{with openldap}
BuildRequires:	openldap-devel
%endif

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%prep
%setup -q
%apply_patches

%build
%serverbuild
%configure2_5x \
	--without-included-regex \
	--without-included-gettext \
	--without-included-zlib \
	--with-static-rnd=linux \
	--without-capabilities \
	--enable-noexecstack \
%ifarch %{sunsparc}
	--enable-m-guard
%else
	--disable-m-guard
%endif
%make

%check
# all tests must pass
make check

%install
%makeinstall_std

sed -e "s#../g10/gpg#gpg#" < tools/lspgpot > %{buildroot}%{_bindir}/lspgpot

sed -i -e 's|/usr/local|/usr/|' %{buildroot}%{_mandir}/man1/gpg.1

# install some extra man pages by debian
install -m0644 debian/gpgsplit.1 %{buildroot}%{_mandir}/man1/
install -m0644 debian/lspgpot.1 %{buildroot}%{_mandir}/man1/

# installed but not wanted
rm -f %{buildroot}%{_datadir}/gnupg/{FAQ,faq.html}
rm -f %{buildroot}%{_datadir}/locale/locale.alias

mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
tar xvjf %{SOURCE2} -C %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS

%find_lang %{name}

%files -f %{name}.lang
%doc README NEWS THANKS TODO doc/DETAILS doc/FAQ doc/HACKING
%doc doc/OpenPGP doc/samplekeys.asc
%doc doc/gpgv.texi
%dir %{_sysconfdir}/RPM-GPG-KEYS
%attr(0644,root,root) %{_sysconfdir}/RPM-GPG-KEYS/*.asc
%attr(0755,root,root) %{_bindir}/gpg
%attr(0755,root,root) %{_bindir}/gpgv
%attr(0755,root,root) %{_bindir}/lspgpot
%attr(0755,root,root) %{_bindir}/gpgsplit
%attr(0755,root,root) %{_bindir}/gpg-zip
%dir %{_libdir}/gnupg
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_curl
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_finger
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_hkp
%if %{with openldap}
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_ldap
%endif
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gnupg1.info*

