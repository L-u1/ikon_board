#!/usr/bin/perl

#############################################################
# Ikonboard v2.1
# Copyright 2001 Ikonboard.com - All Rights Reserved
# Ikonboard is a trademark of Ikonboard.com
#
# Software Distributed by: Ikonboard.com
# Visit us online at http://www.ikonboard.com
# Email us on boards@ikonboard.com
#
# All files written by Matthew Mecham
#############################################################

use CGI::Carp "fatalsToBrowser";          # Output errors to browser
use CGI qw(:standard);                    # Saves loads of work
$CGI::POST_MAX=1024 * 150;                # limit post data
$CGI::DISABLE_UPLOADS = 1;                # Disable uploads

eval {
($0 =~ m,(.*)/[^/]+,)   and unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) and unshift (@INC, "$1");
require "ikon.lib";          # Require ikonboard ()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/styles.cgi";   # Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                        # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "loginout.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;


for ('inmembername','inpassword','action') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
    }


if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }

if ($inmembername eq "") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        }


&title;



$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=top align=left><font face="$font" color=$fontcolormisc size=$dfontsize2>
        <font face="$font" color=$fontcolormisc size=$dfontsize2>
	    &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	    <br>
        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0104'}
        </td>
    </tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>    
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
~;


if ($action eq "login") {

&getmember("$inmembername");

if (($userregistered ne "no") && ($inpassword eq $password)) { 
    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1002'} $inmembername</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
    $ibtxt{'1004'}:
    <ul>
    <li><a href="$forumsummaryprog">$ibtxt{'1003'}</a>
    </ul>
    </tr>
    </td>
    </table></td></tr></table>
    <meta http-equiv="refresh" content="3; url=$forumsummaryprog">
    ~;
    $namecookie = cookie(-name    =>   "amembernamecookie",
                         -value   =>   "$inmembername",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    $passcookie = cookie(-name    =>   "apasswordcookie",
                         -value   =>   "$inpassword",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    print header(-cookie=>[$namecookie, $passcookie]);
    
    }
else {
print header('text/html; charset=windows-1251');
    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1005'}</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize2>
    $ibtxt{'1006'}
    <ul>
    <li>$ibtxt{'0125'}
    <li>$ibtxt{'0126'}
    <li><a href="$registerprog">$ibtxt{'0127'}</a> $ibtxt{'0136'}
    </ul>
    </tr>
    </td>
    </table></td></tr></table>
    
    ~;
    
    }

}

elsif ($action eq "logout") {

    $output .= qq~
    <tr>
    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1011'}</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
    $ibtxt{'1004'}:
    <ul>
    <li><a href="$forumsummaryprog">$ibtxt{'1012'}</a>
    <li>$ibtxt{'1013'}
    </ul>
    </tr>
    </td>
    </table></td></tr></table>
    ~;
        $namecookie = cookie(-name    =>   "amembernamecookie",
                             -path    =>   "$cookiepath",
                             -value   =>   "",
                             -expires =>   "now");
        $passcookie = cookie(-name    =>   "apasswordcookie",
                             -value   =>   "",
                             -path    =>   "$cookiepath",
                             -expires =>   "now");
        $trashcookie = cookie(-name    =>   "templastvisit",
                              -path    =>   "$cookiepath",
                              -value   =>   "",
                              -expires =>   "now");
        print header(-cookie=>[$namecookie, $passcookie, $trashcookie]);
}

else {
print header('text/html; charset=windows-1251');
    $inmembername =~ s/\_/ /g;
    $output .= qq~
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0801'}</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=text name="inmembername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'1417'}</font></a></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
    <td bgcolor=$miscbackone valign=middle><input type=password name="inpassword" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
    ~;
    
}

&output(
-Title   => "$boardname - $ibtxt{'1019'}", 
-ToPrint => $output, 
-Version => $versionnumber 
);

