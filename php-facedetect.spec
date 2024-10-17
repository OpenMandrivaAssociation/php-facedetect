%define modname facedetect
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B17_%{modname}.ini

Summary:	PHP extension to access the OpenCV library
Name:		php-%{modname}
Version:	1.1.0
Release:	2
Group:		Development/PHP
License:	PHP
URL:		https://www.xarg.org/project/php-facedetect/
Source0:	http://www.xarg.org/download/PHP-Facedetect-%{version}.tar.gz
Source1:	B17_facedetect.ini
Patch1:		php7.patch
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	opencv-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension provides a PHP implementation of the OpenCV library.
The extension offers two new functions. In principle, they differ
only by their return value. The first returns only the number of
faces found on the given image and the other an associative array
of their coordinates.

%prep

%setup -q -n PHP-Facedetect-%{version}
%autopatch -p1

sed -i 's/\r//' CREDITS

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-5mdv2012.0
+ Revision: 797101
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-4
+ Revision: 761223
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3
+ Revision: 696416
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2
+ Revision: 695390
- rebuilt for php-5.3.7

* Thu May 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 676197
- fix build
- import php-facedetect


* Thu May 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2010.2
- initial Mandriva package (fedora import)
