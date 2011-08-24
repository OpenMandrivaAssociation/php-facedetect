%define modname facedetect
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B17_%{modname}.ini

Summary:	PHP extension to access the OpenCV library
Name:		php-%{modname}
Version:	1.0.1
Release:	%mkrel 3
Group:		Development/PHP
License:	PHP
URL:		http://www.xarg.org/project/php-facedetect/
Source0:	http://www.xarg.org/download/facedetect-%{version}.tar.gz
Source1:	B17_facedetect.ini
Patch0:		facedetect-dso-link-workaround.patch
Patch1:		facedetect-1.0.1-opencv-2.2.0.patch
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

%setup -q -n facedetect
%patch0 -p1
%patch1 -p1

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

