#!/usr/bin/perl
######################################################################
##  server.cgi - locate and provide information about a server      ##
######################################################################
##  This software is freeware and can be edited and redistributed.  ##
##  This may not work on all Unix servers, it is a quick hack so    ##
##  beginners can try to find out more info about their server      ##
##  without having to bother the sysadmin.                          ##
######################################################################

use strict;
use vars qw(%TPL);

print "Content-type: text/html\n\n";

$TPL{'OPSYS'} = getos();
$TPL{'SSOFT'} = getssoft();
$TPL{'DROOT'} = getdroot();
$TPL{'CUDIR'} = getcudir();
$TPL{'MLLOC'} = getmail();
$TPL{'STIME'} = getstime();
$TPL{'RUSER'} = getruser();
$TPL{'RGRUP'} = getrgrup();
$TPL{'PVERS'} = $];
display();
exit;


sub err {
  my($cause, $file, $fnct) = @_;
  chomp($cause);

  print "<pre>\n" if( $ENV{'REQUEST_METHOD'} );
  print "A CGI ERROR HAS OCCURRED\n========================\n";
  print "Error Message     :  $cause\n";   
  print "Accessing File    :  $file\n";

  exit;
}

sub getos {
  my $os = `uname -sr`;
  if( !$os ) {
    $os = $^O;
    $os =~ s/^(\w)/uc($1)/e;
  }
  return $os ? $os : "<font color='red'>Unknown</font>";
}

sub getssoft {
  return $ENV{'SERVER_SOFTWARE'} ? $ENV{'SERVER_SOFTWARE'} : "<font color='red'>Unknown</font>";
}

sub getdroot {
  return $ENV{'DOCUMENT_ROOT'} ? $ENV{'DOCUMENT_ROOT'} : "<font color='red'>Unknown</font>";
}

sub getcudir {
  my $dir = $ENV{'SCRIPT_FILENAME'};
  $dir =~ s/\/server\.(.*)$//i;
  $dir = "<font color='red'>Unknown</font>" unless(defined $dir);
  my $wdir = `pwd`;

  return $wdir ? $wdir : $dir;
}

sub getmail {
  my @cm = qw( /usr/sbin/sendmail /usr/bin/sendmail /usr/lib/sendmail /var/qmail/bin/qmail-inject );
  for( @cm ) {
    return $_ if( -x $_ );
  }
  return "<font color='red'>Unknown</font>";
}

sub getstime {
  my $time = `date`;
  return $time ? $time : localtime();
}

sub getruser {
  my $user = (getpwuid( $< ))[0];
  return $user ? $user : "<font color='red'>Unknown</font>";
}

sub getrgrup {
  my $group = (getgrgid( $) ))[0];
  return $group ? $group : "<font color='red'>Unknown</font>";
}

sub display {
  print <<__HTML__;
<html>
<head>
  <title>Server Information</title>
<body bgcolor="white" link="blue">

<div align="center">

<table border="0" cellpadding="0" cellspacing="0" width="650">
<tr bgcolor="#000000">
<td align="center">

<table cellspacing="1" cellpadding="3" border="0" width="100%">

<tr>
<td bgcolor="#7384BD" align="center" colspan="2">
<font face="Arial" size="3" color="white">
<b>Commonly Needed Information</b>
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Operating System</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'OPSYS'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Web Server Software</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'SSOFT'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Document Root</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'DROOT'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Current Directory</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'CUDIR'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Sendmail Location</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'MLLOC'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Running As User</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'RUSER'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Running As Group</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'RGRUP'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Perl Version</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana, Arial" size="2">
$TPL{'PVERS'}
</font>
</td>
</tr>

<tr bgcolor="#dcdcdc">
<td width="30%">
<font face="Verdana, Arial" size="2"><b>
Local Server Time</b>
</font>
</td>
<td bgcolor="white" width="70%">
<font face="Verdana,Arial" size="2">
$TPL{'STIME'}
</font>
</td>
</tr>

</table>

</td>
</tr>
</table>

<br><br>

<table width="650">
<tr>
<td>
<font face="Verdana,Arial" size="2">
<b>Document Root:</b> This is the base directory where your HTML files are served from.  When you bring up
your site in your browser (ie http://www.domain.com/index.html), the index.html file is served from this
directory.  This is a full path, and can be used when setting up CGI scripts that require full paths to
directories on your server.
<br><br>
<b>Current Directory:</b> This is the directory that the server.cgi file is currently located in.  This too 
can be useful when setting up CGI scripts that require full paths to directories on your server.  If this 
value looks different than the document root, you should probably use this value over that one.
<br><br>
<b>Sendmail Location:</b> This is the full path and filename of the sendmail executable on your server.  Sendmail is 
often used for sending e-mails from CGI scripts, so if you are ever asked for a path to sendmail on your server, this
is the value you would use.
<br><br>
<b>User/Group:</b> The user and group that the script is running as can be useful in determining what file permissions
are required on your server.  If the user does not match the username that you use to login to the server, you will need
to use more liberal file permissions (777 for directories, 666 for files that need to be written to).  If it is running
as the same user that you login to the server as, you can use more conservative file permissions (755 for directories, and
644 for files that need to be written to).  In either case, CGI scripts should be set to 755 for permissions.
<br><br>
<b>Other Information:</b> The other information listed above can be useful for other reasons.  When you are reporting a
problem to the creator of the CGI software, it will often be helpful to the programmer to know the OS, Perl version, and
server software being used.
</font>
</td>
</tr>
</table>

</body>
</html>
__HTML__
}