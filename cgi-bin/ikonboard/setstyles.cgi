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

$thisprog = "setstyles.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/\///g;
        $_ =~ s/\$//g;
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


        $printme .= "1\;\n";

        $filetomake = "$ikondir" . "data/styles.cgi";

        open(FILE,">$filetomake");
          flock(FILE,2);
        print FILE "$printme";
        close(FILE);
        
         
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b$ibtxt{'0208'}></b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=verdana color=#333333 size=3><center><b>$ibtxt{'2601'}</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
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
                    <font face=verdana color=#333333 size=3><b>$ibtxt{'2106'}</b><br>$ibtxt{'2107'}
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#333333" colspan=2><font face=verdana size=3 color=#FFFFFF>
                <b>$ibtxt{'0208'} / $ibtxt{'0813'}</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=3><b>$ibtxt{'0813'}</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2801'}</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>$ibtxt{'2802'} $ibtxt{'2805'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="titleback" value="$titleback"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>$ibtxt{'2803'} $ibtxt{'2805'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="titlefont" value="$titlefont"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>$ibtxt{'2804'} $ibtxt{'2805'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="titleborder" value="$titleborder"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2806'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="menufontcolor" value="$menufontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2807'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="menubackground" value="$menubackground"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b>$ibtxt{'2808'}</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2809'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"arial\">Arial\n<option value=\"comic sans ms\">Comic Sans MS\n<option value=\"helvetica\">Helvetica\n<option value=\"lucida\">Lucida\n<option value=\"times new roman\">Times New Roman\n<option value=\"verdana\">Verdana\n<option value=\"sans-serif\">Sans-Serif\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2810'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="lastpostfontcolor" value="$lastpostfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2811'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="fonthighlight" value="$fonthighlight"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2812'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                ~;
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"arial\">Arial\n<option value=\"comic sans ms\">Comic Sans MS\n<option value=\"helvetica\">Helvetica\n<option value=\"lucida\">Lucida\n<option value=\"times new roman\">Times New Roman\n<option value=\"verdana\">Verdana\n<option value=\"sans-serif\">Sans-Serif\n</select><p>\n";
                $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
                print qq~
                $tempoutput</td>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2813'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="posternamecolor" value="$posternamecolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2814'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="adminnamecolor" value="$adminnamecolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2815'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="teamnamecolor" value="$teamnamecolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2816'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2817'}
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1>$ibtxt{'2818'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="fontcolormisc" value="$fontcolormisc"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2819'} $ibtxt{'2707'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="miscbackone" value="$miscbackone"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2819'} $ibtxt{'2708'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="miscbacktwo" value="$miscbacktwo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2820'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2821'}
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2822'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="catback" value="$catback"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2823'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="catfontcolor" value="$catfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2824'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="tablebordercolor" value="$tablebordercolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2825'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="tablewidth" value="$tablewidth"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2826'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2827'}
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2828'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="titlecolor" value="$titlecolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2829'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="titlefontcolor" value="$titlefontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2830'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2831'}
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2832'} $ibtxt{'2707'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="forumcolorone" value="$forumcolorone"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2832'} $ibtxt{'2708'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="forumcolortwo" value="$forumcolortwo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2833'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="forumfontcolor" value="$forumfontcolor"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2834'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2835'}
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2836'} $ibtxt{'2707'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="postcolorone" value="$postcolorone"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2836'} $ibtxt{'2708'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="postcolortwo" value="$postcolortwo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2837'} $ibtxt{'2707'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="postfontcolorone" value="$postfontcolorone"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2837'} $ibtxt{'2708'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="postfontcolortwo" value="$postfontcolortwo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>$ibtxt{'2838'}</center></b><br>
                <font face=verdana color=#333333 size=1>$ibtxt{'2839'}
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2840'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="maxthreads" value="$maxthreads"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2841'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="hottopicmark" value="$hottopicmark"></td>
                </tr>
            
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <font face=verdana color=#333333 size=1>$ibtxt{'2842'}</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="boardlogo" value="$boardlogo"></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3><b><center>Графика форума</center></b>
                <font face=verdana color=#333333 size=1>Здесь можно настроить кнопки топика и другие графические элементы форума.
                </td></tr>
                ~;

                $tempoutput = "<select name=\"text_menu\">\n<option value=\"no\">$ibtxt{'2615'}\n<option value=\"yes\">$ibtxt{'2616'}\n</select>\n";
                $tempoutput =~ s/value=\"$text_menu\"/value=\"$text_menu\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=verdana color=#333333 size=1><b>Включить текстовые меню в топиках?</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$newthread" border="0"><br>
                <font face=verdana color=#333333 size=1>Кнопка новой темы</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="newthread" value="$newthread"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$replytothread" border="0"><br>
                <font face=verdana color=#333333 size=1>Кнопка ответа</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="replytothread" value="$replytothread"><font size=1 color=red>(обязательно)</font></td>
                </tr>
       
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$closed" border="0"><br>
                <font face=verdana color=#333333 size=1>Кнопка - тема закрыта</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="closed" value="$closed"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$announce" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка объявлений</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="announce" value="$announce"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$team" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка команды</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="team" value="$team"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$emailtofriend" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - отправь другу</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="emailtofriend" value="$emailtofriend"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$printpage" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - версия для печати</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="printpage" value="$printpage"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$edit" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Правка</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="edit" value="$edit"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$profile" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - профиль</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="profile" value="$profile"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$email" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - E-mail</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="email" value="$email"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$homepagepic" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - домашняя страничка</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="homepagepic" value="$homepagepic"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$message" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Сообщение</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="message" value="$message"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$aol" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - AOL</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="aol" value="$aol"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$icq" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - ICQ</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="icq" value="$icq"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                                                                                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$reply" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Ответить</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="reply" value="$reply"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$part" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - разделитель</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="part" value="$part"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$online" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - В online</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="online" value="$online"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$topichotnonew" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка -  Горячая новая тема</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="topichotnonew" value="$topichotnonew"><font size=1 color=red>(обязательно)</font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$topichot" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Горячая тема</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="topichot" value="$topichot"><font size=1 color=red>(обязательно)</font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$topicnew" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Новая тема</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="topicnew" value="$topicnew"><font size=1 color=red>(обязательно)</font></td>
                </tr>                                                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$topicnonew" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Нет новых сообщений</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="topicnonew" value="$topicnonew"><font size=1 color=red>(обязательно)</font></td>
                </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$topiclocked" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Тема закрыта</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="topiclocked" value="$topiclocked"><font size=1 color=red>(обязательно)</font></td>
                </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$foldernew" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Есть новые темы</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="foldernew" value="$foldernew"><font size=1 color=red>(обязательно)</font></td>
                </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left><img src="$imagesurl/images/$folder" border="0"><br>
                <font face=verdana color=#333333 size=1>Картинка - Нет новых тем</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=30 name="folder" value="$folder"><font size=1 color=red>(обязательно)</font></td>
                </tr>                 
                 
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=verdana color=#333333 size=1>!!! Если оставить не заполненым обязательное поле то картинка будет отображаться как недоступная.
                </td></tr> 
                 
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=verdana color=#990000 size=3>&nbsp;
                
                </td></tr> 
                                                                                                  
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value=$ibtxt{'0039'}></form></td></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }
        
print qq~</td></tr></table></body></html>~;
exit;
