Summary:	Common CA Certificates
Name:		ca-certificates
Version:	20130610
Release:	1
License:	GPL v2 (scripts), MPL v2 (mozilla certs), distributable (other certs)
Group:		Libraries
Source0:	ftp://ftp.debian.org/debian/pool/main/c/ca-certificates/%{name}_%{version}.tar.gz
# Source0-md5:	ca34fb3a5bfb3264062d592c69f1dec6
Patch0:		%{name}-undebianize.patch
Patch1:		%{name}-etc-certs.patch
Patch2:		%{name}-endline.patch
Patch3:		%{name}-DESTDIR.patch
Patch4:		%{name}.d.patch
URL:		http://www.cacert.org/
BuildRequires:	openssl-tools
BuildRequires:	openssl-tools-perl
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certsdir	/etc/certs
%define		openssldir	/etc/openssl/certs

%description
Common CA Certificates.

%package update
Summary:	Script for updating CA Certificates database
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	coreutils
Requires:	openssl-tools

%description update
Script and data for updating CA Certificates database.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i 's,@openssldir@,%{openssldir},' sbin/update-ca-certificates*

%build
%{__make}

# We have those and more in specific dirs
%{__rm} mozilla/{Thawte,thawte,Certum,IGC_A,Deutsche_Telekom_Root_CA_2,Juur-SK}*.crt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sbindir},%{certsdir},%{_sysconfdir}/ca-certificates.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_datadir}/ca-certificates -name '*.crt' -exec sed -i -e 's/\r$//' {} \;

(
cd $RPM_BUILD_ROOT%{_datadir}/ca-certificates
find . -name '*.crt' | sort | cut -b3-
) > $RPM_BUILD_ROOT%{_sysconfdir}/ca-certificates.conf

# build %{certsdir}/ca-certificates.crt
install -d $RPM_BUILD_ROOT%{openssldir}
./sbin/update-ca-certificates --destdir $RPM_BUILD_ROOT
%{__rm} -r $RPM_BUILD_ROOT%{openssldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post update
%{_sbindir}/update-ca-certificates --fresh || :

%files
%defattr(644,root,root,755)
%doc debian/README.Debian debian/changelog
%config(noreplace) %verify(not md5 mtime size) %{certsdir}/ca-certificates.crt

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/update-ca-certificates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ca-certificates.conf
%dir %{_sysconfdir}/ca-certificates.d
%{_datadir}/ca-certificates

