Name: opencryptoki
Summary: Implementation of the PKCS#11 (Cryptoki) specification v3.0
Version: 3.21.0
Release: 9%{?dist}
License: CPL
Group: System Environment/Base
URL: https://github.com/opencryptoki/opencryptoki
Source0: https://github.com/opencryptoki/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# bz#1373833, change tmpfiles snippets from /var/lock/* to /run/lock/*
Patch1: opencryptoki-3.11.0-lockdir.patch
# add missing p11sak_defined_attrs.conf
Patch2: opencryptoki-3.21.0-p11sak.patch
# comment some unsupported sandbox options and add /run to ReadWritePaths to exclude
# /run directory from being made read-only on rhel8
Patch3: opencryptoki-3.21-sandboxing.patch

# upstream patches
# pkcsstats: Fix handling of user name
Patch100: opencryptoki-3.21.0-f4166214552a92d8d66de8011ab11c9c2c6bb0a4.patch
# p11sak: Fix user confirmation prompt behavior when stdin is closed
Patch101: opencryptoki-3.21.0-4ff774568e334a719fc8de16fe2309e2070f0da8.patch
# p11sak: Fix segfault in PEM_write_bio() on OpenSSL 1.1.1
Patch102: opencryptoki-3.21.0-f8ddcd5ba7e5b0bab00dedc89021147ec55b41b3.patch
# p11sak fails as soon as there reside non-key objects
Patch103: opencryptoki-3.21.0-92999f344a3ad99a67a1bcfd9ad28f28c33e51bc.patch
# opencryptoki p11sak tool: slot option does not accept argument 0 for slot index 0
Patch104: opencryptoki-3.21.0-2ba0f41ef5e14d4b509c8854e27cf98e3ee89445.patch

Requires(pre): coreutils diffutils
Requires: (selinux-policy >= 3.14.3-121 if selinux-policy-targeted)
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: openssl-devel >= 1.1.1
BuildRequires: trousers-devel
BuildRequires: openldap-devel
BuildRequires: autoconf automake libtool
BuildRequires: bison flex
BuildRequires: systemd-devel
BuildRequires: libcap-devel
BuildRequires: expect
BuildRequires: make
%ifarch s390 s390x
BuildRequires: libica-devel >= 3.3
%endif
Requires(pre): %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}(token)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the Slot Daemon (pkcsslotd) and general utilities.


%package libs
Group:			System Environment/Libraries
Summary:		The run-time libraries for opencryptoki package
Requires(pre):	shadow-utils

%description libs
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package contains the PKCS#11 library implementation, and requires
at least one token implementation (packaged separately) to be fully
functional.


%package devel
Group:			Development/Libraries
Summary:		Development files for openCryptoki
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the development header files for building
opencryptoki and PKCS#11 based applications


%package swtok
Group:			System Environment/Libraries
Summary:		The software token implementation for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description swtok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the software token implementation to use opencryptoki
without any specific cryptographic hardware.


%package tpmtok
Group:			System Environment/Libraries
Summary:		Trusted Platform Module (TPM) device support for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description tpmtok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
Trusted Platform Module (TPM) devices in the opencryptoki stack.


%package icsftok
Group:			System Environment/Libraries
Summary:		ICSF token support for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description icsftok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support
ICSF token in the opencryptoki stack.


%ifarch s390 s390x
%package icatok
Group:			System Environment/Libraries
Summary:		ICA cryptographic devices (clear-key) support for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description icatok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support ICA
devices in the opencryptoki stack. ICA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"accelerator" or "clear-key" path.

%package ccatok
Group:			System Environment/Libraries
Summary:		CCA cryptographic devices (secure-key) support for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description ccatok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support CCA
devices in the opencryptoki stack. CCA is an interface to IBM
cryptographic hardware such as IBM 4764 or 4765 that uses the
"co-processor" or "secure-key" path.

%package ep11tok
Group:			System Environment/Libraries
Summary:		CCA cryptographic devices (secure-key) support for opencryptoki
Requires(pre):		%{name}-libs%{?_isa} = %{version}-%{release}
Requires:		%{name}-libs%{?_isa} = %{version}-%{release}
Provides:		%{name}(token)

%description ep11tok
Opencryptoki implements the PKCS#11 specification v2.20 for a set of
cryptographic hardware, such as IBM 4764 and 4765 crypto cards, and the
Trusted Platform Module (TPM) chip. Opencryptoki also brings a software
token implementation that can be used without any cryptographic
hardware.
This package brings the necessary libraries and files to support EP11
tokens in the opencryptoki stack. The EP11 token is a token that uses
the IBM Crypto Express adapters (starting with Crypto Express 4S adapters)
configured with Enterprise PKCS#11 (EP11) firmware.
%endif


%prep
%autosetup -p1


%build
./bootstrap.sh

%configure --with-systemd=%{_unitdir}  \
    --with-pkcsslotd-user=pkcsslotd --with-pkcs-group=pkcs11 \
%ifarch s390 s390x
    --enable-icatok --enable-ccatok --enable-ep11tok --enable-pkcsep11_migrate
%else
    --disable-icatok --disable-ccatok --disable-ep11tok --disable-pkcsep11_migrate --disable-pkcscca_migrate
%endif

make %{?_smp_mflags} CHGRP=/bin/true


%install
make install DESTDIR=$RPM_BUILD_ROOT CHGRP=/bin/true

# Remove unwanted cruft
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/stdll/*.la


%post libs -p /sbin/ldconfig
%post swtok -p /sbin/ldconfig
%post tpmtok -p /sbin/ldconfig
%post icsftok -p /sbin/ldconfig
%ifarch s390 s390x
%post icatok -p /sbin/ldconfig
%post ccatok -p /sbin/ldconfig
%post ep11tok -p /sbin/ldconfig
%endif

%postun libs -p /sbin/ldconfig
%postun swtok -p /sbin/ldconfig
%postun tpmtok -p /sbin/ldconfig
%postun icsftok -p /sbin/ldconfig
%ifarch s390 s390x
%postun icatok -p /sbin/ldconfig
%postun ccatok -p /sbin/ldconfig
%postun ep11tok -p /sbin/ldconfig
%endif

%pre
# don't touch opencryptoki.conf even if it is unchanged due to new tokversion
# backup config file
%global cfile /etc/opencryptoki/opencryptoki.conf
%global csuffix .rpmsave.XyoP
if test $1 -gt 1 && test -f %{cfile} ; then
    cp -p %{cfile} %{cfile}%{csuffix}
fi

%pre libs
getent group pkcs11 >/dev/null || groupadd -r pkcs11
getent passwd pkcsslotd >/dev/null || useradd -r -g pkcs11 -d /run/opencryptoki -s /sbin/nologin -c "Opencryptoki pkcsslotd user" pkcsslotd
exit 0

%post
# restore the config file from %pre
if test $1 -gt 1 && test -f %{cfile} ; then
    if ( ! cmp -s %{cfile} %{cfile}%{csuffix} ) ; then
        cp -p %{cfile} %{cfile}.rpmnew
    fi
    cp -p %{cfile}%{csuffix} %{cfile} && rm -f %{cfile}%{csuffix}
fi

%systemd_post pkcsslotd.service
if test $1 -eq 1; then
    %tmpfiles_create
fi

%preun
%systemd_preun pkcsslotd.service

%postun
%systemd_postun_with_restart pkcsslotd.service

%triggerun -- opencryptoki < 3.21.0-1
/usr/bin/systemctl daemon-reload

%files
%doc ChangeLog FAQ README.md
%doc doc/opencryptoki-howto.md
%doc doc/README.token_data
%doc %{_docdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0640, root, pkcs11) %config(noreplace) %{_sysconfdir}/%{name}/p11sak_defined_attrs.conf
%attr(0640, root, pkcs11) %config(noreplace) %{_sysconfdir}/%{name}/strength.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/pkcsslotd.service
%{_sbindir}/p11sak
%{_sbindir}/pkcstok_migrate
%{_sbindir}/pkcsconf
%{_sbindir}/pkcsslotd
%{_sbindir}/pkcsstats
%{_sbindir}/pkcshsm_mk_change
%{_mandir}/man1/p11sak.1*
%{_mandir}/man1/pkcstok_migrate.1*
%{_mandir}/man1/pkcsconf.1*
%{_mandir}/man1/pkcsstats.1*
%{_mandir}/man1/pkcshsm_mk_change.1*
%{_mandir}/man5/policy.conf.5*
%{_mandir}/man5/strength.conf.5*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man5/p11sak_defined_attrs.conf.5*
%{_mandir}/man7/%{name}.7*
%{_mandir}/man8/pkcsslotd.8*
%{_libdir}/opencryptoki/methods
%{_libdir}/pkcs11/methods
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/HSM_MK_CHANGE
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}
%ghost %dir %attr(770,root,pkcs11) %{_rundir}/lock/%{name}/*
%dir %attr(710,pkcsslotd,pkcs11) /run/%{name}

%files libs
%license LICENSE
%{_sysconfdir}/ld.so.conf.d/*
# Unversioned .so symlinks usually belong to -devel packages, but opencryptoki
# needs them in the main package, because:
#   documentation suggests that programs should dlopen "PKCS11_API.so".
%dir %{_libdir}/opencryptoki
%{_libdir}/opencryptoki/libopencryptoki.*
%{_libdir}/opencryptoki/PKCS11_API.so
%dir %{_libdir}/opencryptoki/stdll
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/libopencryptoki.so
%{_libdir}/pkcs11/PKCS11_API.so
%{_libdir}/pkcs11/stdll
%dir %attr(770,root,pkcs11) %{_localstatedir}/log/opencryptoki

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%files swtok
%{_libdir}/opencryptoki/stdll/libpkcs11_sw.*
%{_libdir}/opencryptoki/stdll/PKCS11_SW.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/swtok/TOK_OBJ/

%files tpmtok
%doc doc/README.tpm_stdll
%{_libdir}/opencryptoki/stdll/libpkcs11_tpm.*
%{_libdir}/opencryptoki/stdll/PKCS11_TPM.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/tpm/

%files icsftok
%doc doc/README.icsf_stdll
%{_sbindir}/pkcsicsf
%{_mandir}/man1/pkcsicsf.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_icsf.*
%{_libdir}/opencryptoki/stdll/PKCS11_ICSF.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/icsf/

%ifarch s390 s390x
%files icatok
%{_libdir}/opencryptoki/stdll/libpkcs11_ica.*
%{_libdir}/opencryptoki/stdll/PKCS11_ICA.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/lite/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/lite/TOK_OBJ/

%files ccatok
%doc doc/README.cca_stdll
%config(noreplace) %{_sysconfdir}/%{name}/ccatok.conf
%{_sbindir}/pkcscca
%{_mandir}/man1/pkcscca.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_cca.*
%{_libdir}/opencryptoki/stdll/PKCS11_CCA.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ccatok/TOK_OBJ/

%files ep11tok
%doc doc/README.ep11_stdll
%config(noreplace) %{_sysconfdir}/%{name}/ep11tok.conf
%config(noreplace) %{_sysconfdir}/%{name}/ep11cpfilter.conf
%{_sbindir}/pkcsep11_migrate
%{_sbindir}/pkcsep11_session
%{_mandir}/man1/pkcsep11_migrate.1*
%{_mandir}/man1/pkcsep11_session.1*
%{_libdir}/opencryptoki/stdll/libpkcs11_ep11.*
%{_libdir}/opencryptoki/stdll/PKCS11_EP11.so
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ep11tok/
%dir %attr(770,root,pkcs11) %{_sharedstatedir}/%{name}/ep11tok/TOK_OBJ/
%endif


%changelog
* Tue Jul 18 2023 Than Ngo <than@redhat.com> - 3.21.0-9
- Resolves: #2223588, FTBFS

* Tue Jul 18 2023 Than Ngo <than@redhat.com> - 3.21.0-8
- Related: #2222595, add triggerun to reload daemon

* Fri Jul 14 2023 Than Ngo <than@redhat.com> - 3.21.0-7
- Resolves: #2222595, p11sak tool: slot option does not accept argument 0 for slot index 0
- Resolves: #2222594, p11sak fails as soon as there reside non-key objects

* Tue Jul 04 2023 Than Ngo <than@redhat.com> - 3.21.0-6
- add workaround for segfault in PEM_write_bio() on OpenSSL 1.1.1
Related: #2159741

* Tue Jun 13 2023 Than Ngo <than@redhat.com> - 3.21.0-5
- add requirement on selinux-policy >= 3.14.3-121 for pkcsslotd policy sandboxing
Related: #2159697

* Thu May 25 2023 Than Ngo <than@redhat.com> - 3.21.0-4
- add verify attributes for opencryptoki.conf to ignore the verification
Related: #2159697

* Mon May 22 2023 Than Ngo <than@redhat.com> - 3.21.0-3
- pkcsstats: Fix handling of user name
- p11sak: Fix user confirmation prompt behavior when stdin is closed
Related: #2159697

* Tue May 16 2023 Than Ngo <than@redhat.com> - 3.21.0-2
- add missing /var/lib/opencryptoki/HSM_MK_CHANGE
- disable unsupported sandbox options and add /run to ReadWritePaths to exclude
  /run directory from being made read-only on rhel8
Related: #2159697

* Mon May 15 2023 Than Ngo <than@redhat.com> - 3.21.0-1
- Resolves: #1984865, ep11 and cca: support concurrent HSM master key changes
- Resolves: #2110500, ep11 token: PKCS #11 3.0 - support AES_XTS 
- Resolves: #2111011, cca token: protected key support
- Resolves: #2159697, update to 3.21.0
- Resolves: #2159740, pkcsslotd hardening
- Resolves: #2159741, p11sak support Dilithium and Kyber keys
- Resolves: #2159742, ica and soft tokens: PKCS #11 3.0 - support AES_XTS

* Mon Jan 30 2023 Than Ngo <than@redhat.com> - 3.19.0-2
- Resolves: #2043856, Support of ep11 token for new IBM Z Hardware (IBM z16)

* Tue Nov 01 2022 Than Ngo <than@redhat.com> - 3.19.0-1
- Resolves: #2126612, opencryptoki fails after generating > 500 RSA keys
- Resolves: #2110315, rebase to 3.19.0
- Resolves: #2110990, openCryptoki key generation with expected MKVP only on CCA and EP11 tokens
- Resolves: #2110477, openCryptoki ep11 token: master key consistency
- Resolves: #1984871, openCryptoki ep11 token: vendor specific key derivation

* Mon Aug 01 2022 Than Ngo <than@redhat.com> - 3.18.0-3
- Related: #2043854, do not touch opencryptoki.conf if it is in place already and even if it is unchanged
- Resolves: #2112785, EP11: Fix C_GetMechanismList returning CKR_BUFFER_TOO_SMALL

* Tue Jun 07 2022 Than Ngo <than@redhat.com> - 3.18.0-2
- Related: #2043854, fix json output

* Tue May 24 2022 Than Ngo <than@redhat.com> - 3.18.0-1
- Resolves: #2043845, rebase to 3.18.0
- Resolves: #2043854, add crypto counters
- Resolves: #2043855, support crypto profiles

* Fri Apr 15 2022 Than Ngo <than@redhat.com> - 3.17.0-4
- Resolves: #2066762, Dilithium support not available 

* Mon Jan 17 2022 Than Ngo <than@redhat.com> - 3.17.0-3
- Resolves: #2040677, API: Unlock GlobMutex if user and group check fails

* Tue Nov 09 2021 Than Ngo <than@redhat.com> - 3.17.0-2
- Related: #1984993, add missing p11sak_defined_attrs.conf 

* Tue Oct 19 2021 Than Ngo <than@redhat.com> - 3.17.0-1
- Resolves: #1984993, rebase to 3.17.0
- Resolves: #1984870, openCryptoki key management tool

* Mon Sep 13 2021 Than Ngo <than@redhat.com> - 3.16.0-6
- Fix: Could not open /run/lock/opencryptoki/LCK..APIlock

* Thu Aug 19 2021 Than Ngo <than@redhat.com> - 3.16.0-5
- Resolves: #1987256, pkcstok_migrate leaves options with multiple strings in opencryptoki.conf options without double-quotes

* Fri Jul 16 2021 Than Ngo <than@redhat.com> - 3.16.0-4
- Resolves: #1964304, Fix detection if pkcsslotd is still running

* Tue Jun 15 2021 Than Ngo <than@redhat.com> - 3.16.0-3
- Related: #1919223, add conditional requirement

* Fri Jun 11 2021 Than Ngo <than@redhat.com> - 3.16.0-2
- Related: #1919223, add requirement on selinux-policy >= 3.14.3-70 for using ipsec

* Tue Jun 01 2021 Than Ngo <than@redhat.com> - 3.16.0-1
- Resolves: #1919223, rebase to 3.16.0
- Resolves: #1922195, Event Notification Support
- Resolves: #1959936, Soft token does not check if an EC key is valid
- Resolves: #1851104, import and export of secure key objects
- Resolves: #1851106, openCryptoki ep11 token: protected key support
- Resolves: #1851107, openCryptoki ep11 token: support attribute bound keys

* Fri Feb 12 2021 Than Ngo <than@redhat.com> - 3.15.1-5
- Resolves: #1928120, Fix problem with C_Get/SetOperationState and digest contexts

* Fri Feb 12 2021 Than Ngo <than@redhat.com> - 3.15.1-4
- Resolves: #1927745, pkcscca migration fails with usr/sb2 is not a valid slot ID

* Thu Nov 26 2020 Than Ngo <than@redhat.com> - 3.15.1-3
- Resolves: #1902022
   Fix compiling with c++
   Added error message handling for p11sak remove-key command

* Thu Nov 26 2020 Than Ngo <than@redhat.com> - 3.15.1-2
- Related: #1847433, Added error message handling for p11sak remove-key command

* Mon Nov 02 2020 Than Ngo <than@redhat.com> - 3.15.1-1
- Related: #1847433
  upstream fixes:
    - Free generated key in all error cases
    - CCA: Zeroize key buffer to avoid CCA 8/32 error
    - Do not delete the map-btree entry if destroying an object is not allowed
    - Remove now unused header timeb.h
    - TESTCASES: Use FIPS conforming keys for 3DES CBC-MAC test vectors
    - Fix buffer overrun in C_CopyObject
    - TPM: Fix double free in openssl_gen_key

* Mon Oct 19 2020 Than Ngo <than@redhat.com> - 3.15.0-1
- Resolves: #1847433, rebase to 3.15.0 
- Resolves: #1851105, PKCS #11 3.0 - baseline provider support
- Resolves: #1851108, openCryptoki ep11 token: enhanced functionality
- Resolves: #1851109, openCryptoki key management tool: key deletion function

* Mon Jul 06 2020 Than Ngo <than@redhat.com> - 3.14.0-5
- Related: #1853420, more fixes

* Fri Jul 03 2020 Than Ngo <than@redhat.com> - 3.14.0-4
- Resolves: #1853420, endian issue 

* Mon Jun 15 2020 Than Ngo <than@redhat.com> - 3.14.0-3
- Resolves: #1780294, PIN conversion tool

* Tue May 26 2020 Than Ngo <than@redhat.com> - 3.14.0-2
- Related: #1780293, fix regression, segfault in C_SetPin

* Tue May 19 2020 Than Ngo <than@redhat.com> - 3.14.0-1
- Resolves: #1723863 - ep11 token: Enhanced Support
- Resolves: #1780285 - ep11 token: Support for new IBM Z hardware z15
- Resolves: #1780293 - rebase to 3.14.0
- Resolves: #1800549 - key management tool: list keys function
 -Resolves: #1800555 - key management tool: random key generation function

* Fri Dec 13 2019 Than Ngo <than@redhat.com> - 3.12.1-2
- Resolves: #1782445, EP11: Fix EC-uncompress buffer length

* Thu Nov 28 2019 Than Ngo <than@redhat.com> - 3.12.1-1
- Resolves: #1777313, rebase to 3.12.1

* Tue Nov 12 2019 Than Ngo <than@redhat.com> - 3.12.0-1
- Resolves: #1726243, rebase to 3.12.0

* Mon Aug 26 2019 Dan Horák <dhorak@redhat.com> - 3.11.1-2
- Resolves: #1739433, ICA HW token missing after the package update

* Mon May 06 2019 Than Ngo <than@redhat.com> - 3.11.1-1
- Resolves: #1706140, rebase to 3.11.1

* Tue Mar 26 2019 Than Ngo <than@redhat.com> - 3.11.0-3
- Resolves: #1667941, 3des tests failures due to FIPS incompatible test scenarios
- Resolves: #1651731, ep11 token: enhanced IBM z14 functions
- Resolves: #1651732, ep11 token: support m_*Single functions from ep11 lib
- Resolves: #1525407, use CPACF hashes in ep11 token
- Resolves: #1651238, rebase to 3.11.0
- Resolves: #1682530, gating

* Fri Dec 14 2018 Than Ngo <than@redhat.com> - 3.10.0-3
- Resolves: #1657683, can't establish libica token in FIPS mode
- Resolves: #1652856, EP11 token fails when using Strict-Session mode or VHSM-Mode

* Thu Oct 25 2018 Than Ngo <than@redhat.com> - 3.10.0-2
- Resolves: #1602641, covscan

* Tue Jun 12 2018 Dan Horák <dan[at]danny.cz> - 3.10.0-1
- Rebase to 3.10.0

* Fri Feb 23 2018 Dan Horák <dan[at]danny.cz> - 3.9.0-1
- Rebase to 3.9.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 24 2017 Dan Horák <dan[at]danny.cz> - 3.8.2-2
- use upstream tmpfiles config

* Thu Nov 23 2017 Dan Horák <dan[at]danny.cz> - 3.8.2-1
- Rebase to 3.8.2 (#1512678)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Sinny Kumari <sinny@redhat.com> - 3.7.0-1
- Rebase to 3.7.0
- Added libitm-devel as BuildRequires

* Mon Apr 03 2017 Sinny Kumari <sinny@redhat.com> - 3.6.2-1
- Rebase to 3.6.2
- RHBZ#1424017 - opencryptoki: FTBFS in rawhide

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 01 2016 Jakub Jelen <jjelen@redhat.com> - 3.5.1-1
- New upstream release

* Tue May 03 2016 Jakub Jelen <jjelen@redhat.com> - 3.5-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Jakub Jelen <jjelen@redhat.com> 3.4.1-1
- New bugfix upstream release

* Wed Nov 18 2015 Jakub Jelen <jjelen@redhat.com> 3.4-1
- New upstream release
- Adding post-release patch fixing compile warnings

* Thu Aug 27 2015 Jakub Jelen <jjelen@redhat.com> 3.3-1.1
- New upstream release
- Correct dependencies for group creation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Jakub Jelen <jjelen@redhat.com> 3.2-3
- Few more undefined symbols fixed for s390(x) specific targets
- Do not require --no-undefined, because s390(x) requires some

* Mon May 04 2015 Jakub Jelen <jjelen@redhat.com> 3.2-2
- Fix missing sources and libraries in makefiles causing undefined symbols (#1193560)
- Make inline function compatible for GCC5

* Wed Sep 10 2014 Petr Lautrbach <plautrba@redhat.com> 3.2-1
- new upstream release 3.2
- add new sub-package opencryptoki-ep11tok on s390x

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Petr Lautrbach <plautrba@redhat.com> 3.1-1
- new upstream release 3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 17 2014 Petr Lautrbach <plautrba@redhat.com> 3.0-10
- create the right lock directory for cca tokens (#1054442)

* Wed Jan 29 2014 Petr Lautrbach <plautrba@redhat.com> 3.0-9
- use Requires(pre): opencryptoki-libs for subpackages

* Mon Jan 20 2014 Dan Horák <dan[at]danny.cz> - 3.0-8
- include token specific directories (#1013017, #1045775, #1054442)
- fix pkcsconf crash for non-root users (#10054661)
- the libs subpackage must care of creating the pkcs11 group, it's the first to be installed

* Tue Dec 03 2013 Dan Horák <dan[at]danny.cz> - 3.0-7
- fix build with -Werror=format-security (#1037228)

* Fri Nov 22 2013 Dan Horák <dan[at]danny.cz> - 3.0-6
- apply post-3.0 fixes (#1033284)

* Tue Nov 19 2013 Dan Horák <dan[at]danny.cz> - 3.0-5
- update opencryptoki man page (#1001729)

* Fri Aug 23 2013 Dan Horák <dan[at]danny.cz> - 3.0-4
- update unit file (#995002)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Dan Horák <dan[at]danny.cz> - 3.0-2
- update pkcsconf man page (#948460)

* Mon Jul 22 2013 Dan Horák <dan[at]danny.cz> - 3.0-1
- new upstream release 3.0

* Tue Jun 25 2013 Dan Horák <dan[at]danny.cz> - 2.4.3.1-1
- new upstream release 2.4.3.1

* Fri May 03 2013 Dan Horák <dan[at]danny.cz> - 2.4.3-1
- new upstream release 2.4.3

* Thu Apr 04 2013 Dan Horák <dan[at]danny.cz> - 2.4.2-4
- enable hardened build
- switch to systemd macros in scriptlets (#850240)

* Mon Jan 28 2013 Dan Horák <dan[at]danny.cz> - 2.4.2-3
- add virtual opencryptoki(token) Provides to token modules and as Requires
  to main package (#904986)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Dan Horák <dan[at]danny.cz> - 2.4.2-1
- new upstream release 2.4.2
- add pkcs_slot man page
- don't add root to the pkcs11 group

* Mon Jun 11 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-2
- fix unresolved symbols in TPM module (#830129)

* Sat Feb 25 2012 Dan Horák <dan[at]danny.cz> - 2.4.1-1
- new upstream release 2.4.1
- convert from initscript to systemd unit
- import fixes from RHEL-6 about root's group membership (#732756, #730903)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 07 2011 Dan Horák <dan[at]danny.cz> - 2.4-1
- new upstream release 2.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Dan Horák <dan[at]danny.cz> 2.3.3-1
- new upstream release 2.3.3

* Tue Nov 09 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.2-2
- Apply Obsoletes to package names, not provides.

* Tue Sep 14 2010 Dan Horák <dan[at]danny.cz> 2.3.2-1
- new upstream release 2.3.2
- put STDLLs in separate packages to match upstream package design

* Thu Jul 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-7
- Move the LICENSE file to the -libs subpackage.

* Tue Jun 29 2010 Dan Horák <dan[at]danny.cz> 2.3.1-6
- rebuilt with CCA enabled (#604287)
- fixed issues from #546274

* Fri Apr 30 2010 Dan Horák <dan[at]danny.cz> 2.3.1-5
- fixed one more issue in the initscript (#547324)

* Mon Apr 26 2010 Dan Horák <dan[at]danny.cz> 2.3.1-4
- fixed pidfile creating and usage (#547324)

* Mon Feb 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-3
- Also list 'reload' and 'force-reload' in "Usage: ...".

* Mon Feb 08 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-2
- Support 'force-reload' in the initscript.

* Wed Jan 27 2010 Michal Schmidt <mschmidt@redhat.com> 2.3.1-1
- New upstream release 2.3.1.
- opencryptoki-2.3.0-fix-nss-breakage.patch was merged.

* Fri Jan 22 2010 Dan Horák <dan[at]danny.cz> 2.3.0-5
- made pkcsslotd initscript LSB compliant (#522149)

* Mon Sep 07 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-4
- Added opencryptoki-2.3.0-fix-nss-breakage.patch on upstream request.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.0-3
- rebuilt with new openssl

* Sun Aug 16 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-2
- Require libica-2.0.

* Fri Aug 07 2009 Michal Schmidt <mschmidt@redhat.com> 2.3.0-1
- New upstream release 2.3.0:
  - adds support for RSA 4096 bit keys in the ICA token.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-5
- Require arch-specific dependency on -libs.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-4
- Return support for crypto hw on s390.
- Renamed to opencryptoki.
- Simplified multilib by putting libs in subpackage as suggested by Dan Horák.

* Tue Jul 21 2009 Michal Schmidt <mschmidt@redhat.com> - 2.2.8-2
- Fedora package based on RHEL-5 package.
