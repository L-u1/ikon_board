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
require "ikonadmin.lib";     # Require Admin func()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/styles.cgi";   # Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "setbadwords.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;


$wordarray     = $query -> param('wordarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

print header('text/html; charset=windows-1251');

&admintitle;
            

if ($action eq "process") {
        
        &getmember("$inmembername");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) { 
        
        $wordarray =~ s/\n\n//g;
        $wordarray =~ s/\n/\&/g;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$ikondir" . "data/badwords.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#333333 size=3><center><b>$ibtxt{'2102'}</b></center><br><br>
                <font size=2><b>$ibtxt{'2103'}</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($bad, $good) = split(/\=/,$_);
                    print qq(<b>$bad</b> $ibtxt{'2104'} <b>$good</b><br>);
                    }
                print qq(
                <br><br><br><center><a href="setbadwords.cgi">$ibtxt{'2105'}</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                    <b>$ibtxt{'0208'}</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                    <font face=verdana color=#333333 size=3><b>$ibtxt{'2106'}</b><br>$ibtxt{'2107'}
                    </td></tr></table></td></tr></table>
                    );
                    }
                }
               }
        
    else {
        
        &getmember("$inmembername");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {
                # Open the badword file

                $filetoopen = "$ikondir" . "data/badwords.cgi";
                open (FILE, "$filetoopen") or $badwords = "damn=d*amn\nhell=h*ll";
                $badwords = <FILE> if (!$badwords);
                close (FILE);
                
                $badwords =~ s/\&/\n/g;
                
                
                $inmembername =~ s/\_/ /g;
                

                print qq(
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2108'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2108'}</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=verdana color=#000000 size=2>
                $ibtxt{'2109'}<br><br>
                <b>$ibtxt{'2110'}</b>damn=d*mn<br><br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=6 wrap="virtual" name="wordarray">$badwords</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit ></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></td></tr></table></td></tr></table></body></html>~;
exit;
