Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	1.4.10
Release:	%mkrel 1
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source:		ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2.sig
Source2:	mdk-keys.tar.bz2
Source3:	mdk-keys.tar.bz2.sig
Patch1:		gnupg-1.4.2.2-use-agent-by-default.diff
Patch4:		gnupg-1.4.5-ppc64.patch
# splitted off from the previous debian patch
Patch6:		gnupg-1.4.7-deb-free_caps.patch
Patch7:		gnupg-1.4.7-deb-manpage.patch
Patch8:		gnupg-1.4.7-deb-min_privileges.patch
Patch10:	gnupg-1.4.6-dir.patch
Requires(post): info-install
Requires(preun): info-install
BuildRequires:	bzip2-devel
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	libcurl-devel >= 7.10
BuildRequires:	libtermcap-devel
BuildRequires:	libusb-devel
BuildRequires:	openldap-devel
BuildRequires:	perl
BuildRequires:	readline-devel
BuildRequires:	sendmail-command
BuildRequires:	bison
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%prep

%setup -q
%patch1 -p0 -b .use_agent
%patch4 -p1 -b .ppc64
%patch6 -p1 -b .free_caps
%patch7 -p1 -b .manpage
%patch8 -p1 -b .min_privileges
%patch10 -p1 -b .dir

%build
%serverbuild
%configure2_5x \
	--without-included-regex \
	--without-included-gettext \
	--without-included-zlib \
	--with-static-rnd=linux \
	--disable-rpath \
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
rm -rf %{buildroot}

%makeinstall_std

sed -e "s#../g10/gpg#gpg#" < tools/lspgpot > %{buildroot}%{_bindir}/lspgpot

perl -pi -e 's|/usr/local|/usr/|' %{buildroot}%{_mandir}/man1/gpg.1

# install some extra man pages by debian
install -m0644 debian/gpgsplit.1 %{buildroot}%{_mandir}/man1/
install -m0644 debian/lspgpot.1 %{buildroot}%{_mandir}/man1/

# installed but not wanted
rm -f %{buildroot}%{_datadir}/gnupg/{FAQ,faq.html}
rm -f %{buildroot}%{_datadir}/locale/locale.alias

mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
tar xvjf %{SOURCE2} -C %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS

%{find_lang} %{name}

%post
%_install_info gnupg1.info
/bin/true

%postun
%_remove_install_info gnupg1.info
/bin/true

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS THANKS TODO doc/DETAILS doc/FAQ doc/HACKING
%doc doc/faq.html doc/OpenPGP doc/samplekeys.asc
%doc doc/gpgv.texi
%attr(4755,root,root) %{_bindir}/gpg
%attr(0755,root,root) %{_bindir}/gpgv
%attr(0755,root,root) %{_bindir}/lspgpot
%attr(0755,root,root) %{_bindir}/gpgsplit
%attr(0755,root,root) %{_bindir}/gpg-zip
%dir %{_libdir}/gnupg
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_curl
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_finger
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_hkp
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_ldap
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gnupg1.info*
%dir %{_sysconfdir}/RPM-GPG-KEYS
%attr(0644,root,root) %{_sysconfdir}/RPM-GPG-KEYS/*.asc
