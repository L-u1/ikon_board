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
require "data/membertitles.cgi";
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "setmembertitles.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

	@params = $query->param;
	foreach (@params) {
        $theparam =~ s/\///g;
        $_ =~ s/\$//g;
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");


print header('text/html; charset=windows-1251');
&admintitle;
          

if ($action eq "process") {

        &getmember("$inmembername");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) { 

        $endprint = "1\;\n";

        $filetomake = "$ikondir" . "data/membertitles.cgi";

        open(FILE,">$filetomake");
          flock(FILE,2);
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        
        if (-e $filetomake && -w $filetomake) {
                 print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'2102'}</b>
                </td></tr></table></td></tr></table>
                ~;
            }

        else {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>{'2106'}</b><br>{'2107'}
                </td></tr></table></td></tr></table>
                ~;
            }
        
        }
    }  
     
else {
        
        &getmember("$inmembername");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) { 
                
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'0815'}</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2702'} $ibtxt{'2707'} $ibtxt{'2701'}</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 1 $ibtxt{'2703'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark1" value="$mpostmark1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 1 $ibtxt{'2404'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle1" value="$mtitle1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 1 $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic1" value="$mgraphic1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2702'} $ibtxt{'2708'} $ibtxt{'2701'}</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 2 $ibtxt{'2703'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark2" value="$mpostmark2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 2 $ibtxt{'2404'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle2" value="$mtitle2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 2 $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic2" value="$mgraphic2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2702'} $ibtxt{'2709'} $ibtxt{'2701'}</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 3 $ibtxt{'2703'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark3" value="$mpostmark3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 3 $ibtxt{'2404'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle3" value="$mtitle3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 3 $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic3" value="$mgraphic3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2702'} $ibtxt{'2710'} $ibtxt{'2701'}</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 4 $ibtxt{'2703'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark4" value="$mpostmark4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 4 $ibtxt{'2404'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle4" value="$mtitle4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 4 $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic4" value="$mgraphic4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2702'} $ibtxt{'2711'} $ibtxt{'2701'}</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 5 $ibtxt{'2703'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark5" value="$mpostmark5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 5 $ibtxt{'2404'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle5" value="$mtitle5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2702'} 5 $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic5" value="$mgraphic5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2706'} $ibtxt{'2705'}</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2706'} $ibtxt{'2705'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="admingraphic" value="$admingraphic"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit ></form></td></tr></table></td></tr></table>
                ~;
                
                }
                else {
                    &adminlogin;
                    }
        
        }
        
print qq~</td></tr></table></body></html>~;
exit;
