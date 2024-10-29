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

$thisprog = "setvariables.cgi";


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

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$ikondir" . "data/boardinfo.cgi";

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
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=verdana color=#333333 size=3><center><b>$ibtxt{'2601'}</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
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
                    <font face=verdana color=#333333 size=3><b>$ibtxt{'2106'}</b><br>$ibtxt{'2107'}<br>$ibtxt{'2602'}.
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'2603'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2604'}</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2605'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2606'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2607'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2608'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2609'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2610'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2611'}</b><br>$ibtxt{'2612'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2613'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2614'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="ikondir" value="$ikondir"></td>
                </tr>
                ~;
                
        		$tempoutput = "<select name=\"membernamefilter\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";                 
				$tempoutput =~ s/value=\"$membernamefilter\"/value=\"$membernamefilter\" selected/;                 
				print qq~
				<tr>                 
				<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
				<font face=verdana color=#333333 size=1><b>$ibtxt{'9990'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>                 
				$tempoutput</td>                 
				</tr>                 
				~;
                
                
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2617'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                
                $tempoutput = "<select name=\"locations_in_topic\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$locations_in_topic\"/value=\"$locations_in_topic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Показывать \"Откуда\" в топиках?</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<input type=text size=2 maxlength=2 name=\"char_locat_in_topic\" value=\"$char_locat_in_topic\">";
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Количество символов в поле \"Откуда\" будет выводиться в топпике.</b><br><i>Вычисляется эксперементально от ширины топика.</i> Default =18</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<input type=text size=3 maxlength=3 name=\"char_in_topic\" value=\"$char_in_topic\">";
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Максимальное длиинное слово в сообщении и в названиии, описании топика.</b><br>Если слово больше - пробел поставится принудительно. <i>Вычисляется эксперементально от ширины топика.</i><br>Default =80</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pips\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$pips\"/value=\"$pips\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Показывать \"Рейтинги\" пользователей в топиках?</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"iplog\">\n<option value=\"on\">Логируется и показывается всем\n<option value=\"lnk\">Логируется, показывается команде\n<option value=\"off\">Выключен\n</select>\n";
                $tempoutput =~ s/value=\"$iplog\"/value=\"$iplog\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Показывать IP пользователей в топиках?</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2618'}</b><br>$ibtxt{'2619'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2620'}</b>
                </font></td>
                </tr>
                ~;
                
                

                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2621'}</b><br>$ibtxt{'2622'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">$ibtxt{'2623'}\n<option value=\"send_mail\">$ibtxt{'2624'}\n<option value=\"blat_mail\">$ibtxt{'2625'}\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2626'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2627'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SEND_MAIL" value="$SEND_MAIL"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2628'}</b><br>'localhost' $ibtxt{'2629'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2630'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2631'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2632'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2633'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
<tr>                 
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>                 
		<font face=verdana color=#990000 size=3><b>$ibtxt{'9998'}</b>                		</font>
		</td>                 
		</tr
		
                <tr>
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
		<font face=verdana color=#333333 size=1>            
		<a href="help/admin/fontsizing.html" target="_blank">$ibtxt{'9997'}</a>
		</font></td>
		</tr>

		<tr>                 
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
		<font face=verdana color=#333333 size=1><b>$ibtxt{'9996'} 1</b> - $ibtxt{'9995'}
		</font>
		</td>                 

		<td bgcolor=#FFFFFF valign=middle align=left>                 
		<input type=text size=2 maxlength=2 name="dfontsize1" value="$dfontsize1">
		</td>                 
		</tr>
                
		<tr>                 
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
		<font face=verdana color=#333333 size=1><b>$ibtxt{'9996'} 2</b> - $ibtxt{'9994'}
		</font>
		</td>                 

		<td bgcolor=#FFFFFF valign=middle align=left>                 
		<input type=text size=2 maxlength=2 name="dfontsize2" value="$dfontsize2">
		</td>                 
		</tr>                 

		<tr>                 
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
		<font face=verdana color=#333333 size=1><b>$ibtxt{'9996'} 3</b> - $ibtxt{'9993'}
		</font>
		</td>                 
		<td bgcolor=#FFFFFF valign=middle align=left>                 
		<input type=text size=2 maxlength=2 name="dfontsize3" value="$dfontsize3">
		</td>                 
		</tr>  
               
		<tr>                 
		<td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
		<font face=verdana color=#333333 size=1><b>$ibtxt{'9996'} 4</b> - $ibtxt{'9992'}
		</font>
		</td>                 

		<td bgcolor=#FFFFFF valign=middle align=left>                 
		<input type=text size=2 maxlength=2 name="dfontsize4" value="$dfontsize4">
		</td>                 
		</tr> 
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2634'}</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"on\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2635'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2636'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="floodcontrollimit" value="$floodcontrollimit"></td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2637'}</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2638'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                ~;

                $tempoutput = "<select name=\"announcements\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>$ibtxt{'2639'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"advanced_folder\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$advanced_folder\"/value=\"$advanced_folder\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Отдельные иконки для каждого форума</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"online_\">\n<option value=\"on\">$ibtxt{'2616'}\n<option value=\"off\">$ibtxt{'2615'}\n<option value=\"reg\">Только для зарегистрированных\n</select>\n";
                $tempoutput =~ s/value=\"$online_\"/value=\"$online_\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Кто в онлайн на главной странице.</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Кол-во минут при подсчете "Кто в онлайн"</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=3 name="membergone" value="$membergone"></td>
                </tr>
                ~;                
                
                $tempoutput = "<select name=\"maintenancemode\">\n<option value=\"n\">NO\n<option value=\"y\">YES\n</ select>\n";                 
                $tempoutput =~ s/value=\"$maintenancemode\"/value=\"$maintenancemode\" selected/;                 
                print qq~          
                <tr>                 
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
                <font face=verdana color=#333333 size=1><b>$ibtxt{'9991'}</b><br></font></td>                 
                <td bgcolor=#FFFFFF valign=middle align=left>                 
                $tempoutput</td>
                </tr> 
                ~;
                
                $tempoutput = "<TEXTAREA wrap=\"virtual\" NAME=\"maintenance_message\" ROWS=\"5\" COLS=\"40\">$maintenance_message</TEXTAREA>\n";                 
                print qq~          
                <tr>                 
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>                 
                <font face=verdana color=#333333 size=1><b>Сообщение которое будет выводиться когда форум закрыт</b><br></font></td>                 
                <td bgcolor=#FFFFFF valign=middle align=left>                 
                $tempoutput</td>
                </tr> 
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value=$ibtxt{'0039'} ></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
