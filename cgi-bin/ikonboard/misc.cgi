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

$thisprog = "misc.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;
	
$UIN                    = $query -> param('UIN');
$action                 = $query -> param('action');
$aimname                = $query -> param('aimname');
$aimname =~ s/ //g;

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }

if (!$inmembername) { $inmembername = "$ibtxt{'0043'}"; }

### Do smilies

if ($action eq "showsmilies") {

    $emoticonsurl = qq~$imagesurl/emoticons~;

    # Set up the HTML, and title
    
    $output = qq~
    
    <html><head><title>$ibtxt{'1201'}</title></head>
    <body topmargin=0 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=#$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor="$titlecolor" align=center valign=middle colspan=2>
                    <font face="$font" color="$titlefontcolor" size=$dfontsize2><b>$boardname - $ibtxt{'1201'}</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbacktwo" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>$ibtxt{'1202'}</font>
                </td>
                    <td bgcolor="$miscbacktwo" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>$ibtxt{'1203'}</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>:)</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$emoticonsurl/smile.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>:(</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$emoticonsurl/sad.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>;)</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$emoticonsurl/wink.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>:o</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$emoticonsurl/shocked.gif" border=0></font>
                </td>
                </tr>
                ~;
    
    # Grab and print them
    
    $dirtoopen = "$imagesdir" . "emoticons";
    opendir (DIR, "$dirtoopen") or die "$ibtxt{'1204'} $dirtoopen )"; 
    @dirdata = readdir(DIR);
    closedir (DIR);


    @emoticondata = grep(/gif/,@dirdata);
    @emoticondata = sort @emoticondata;
        
    foreach $picture (@emoticondata) {
    $smileyname = $picture;
    $smileyname =~ s/\.gif//g;
    
    $output .= qq~
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>:$smileyname:</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$emoticonsurl/$picture" border=0></font>
                </td>
                </tr>
                ~;
    } #endforeach


    $output .= qq~
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;

} # end if smilies action


### ICQ stuff

elsif ($action eq "icq") {
$UIN=&cleaninput($UIN);  #пофиксили уязвимость пейджера
$output = qq~
    
    <html><head><title>$ibtxt{'1205'} $boardname</title></head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <form action="http://wwp.mirabilis.com/scripts/WWPMsg.dll" method="post">
        <input type="hidden" name="subject" value="From $boardname"><input type="hidden" name="to" value="$UIN">
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor="$titlecolor" align=center valign=middle colspan=2>
                    <font face="$font" color="$titlefontcolor" size=$dfontsize2><b>$boardname - $ibtxt{'1207'}</b><br>$ibtxt{'1206'} $UIN</font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbacktwo" align=left valign=top>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>$ibtxt{'0922'}</font>
                </td>
                    <td bgcolor="$miscbacktwo" align=left valign=middle>
                    <input type="text" name="from" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=left valign=top>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>$ibtxt{'1209'}</font>
                </td>
                    <td bgcolor="$miscbackone" align=left valign=middle>
                    <input type="text" name="fromemail" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=left valign=top>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>$ibtxt{'1210'}</font>
                </td>
                    <td bgcolor="$miscbackone" align=left valign=middle>
                    <textarea name="body" rows="3" cols="30" wrap="Virtual"></textarea>
                </td>
                </tr>
                <tr>
                <td bgcolor="$miscbacktwo" align=center valign=middle colspan=2>
                <input type="submit" name="Send" value="$ibtxt{'1211'}"></form>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
    
} # end elsif icq



elsif ($action eq "ikoncode") {

$output = qq~
    
    <html><head><title>$ibtxt{'1212'}</title></head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1 border=0>
            <tr>
                <td bgcolor="$titlecolor" align=center valign=middle colspan=2>
                    <font face="$font" color="$titlefontcolor" size=$dfontsize2><b>$ibtxt{'1213'}</b>
                    <br>$ibtxt{'1214'}
                    </font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>
                    <font color=$fonthighlight>[quote]</font>$ibtxt{'1215'}<font color=$fonthighlight>[/quote]</font><br>Также можно пользоваться тэгом <font color=$fonthighlight>[q][/q]</font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><hr size=1 noshade color=$fonthighlight><blockquote><font size=-1>$ibtxt{'1215'}</blockquote><hr noshade size=1 color=$fonthighlight></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[url]</font>http://www.ikonboard.com<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><a href="http://www.ikonboard.com">http://www.ikonboard.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[url=http://www.ikonboard.com</font>Ikonboard<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><a href="http://www.ikonboard.com">Ikonboard</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[email=ikonboard\@ikonboard.com]</font>$ibtxt{'1217'}<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><a href="mailto:ikonboard\@ikondiscussion.com">$ibtxt{'1217'}</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[b]</font>$ibtxt{'1218'}<font color=$fonthighlight>[/b]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><b>$ibtxt{'1218'}</b></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[c]</font>Центрированный текст<font color=$fonthighlight>[/c]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><center>Центрированный текст</center></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[s]</font>Мелкий текст<font color=$fonthighlight>[/s]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><small>Мелкий текст</small></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[i]</font>$ibtxt{'1219'}<font color=$fonthighlight>[/i]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><i>$ibtxt{'1219'}</i></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[u]</font>$ibtxt{'1220'}<font color=$fonthighlight>[/u]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><u>$ibtxt{'1220'}</u></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[size=4]</font>$ibtxt{'1221'}<font color=$fonthighlight>[/size]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font size=$dfontsize4>$ibtxt{'1221'}</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[font=impact]</font>$ibtxt{'1222'}<font color=$fonthighlight>[/font]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font face=impact>$ibtxt{'1222'}</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[color=red]</font>$ibtxt{'1223'}<font color=$fonthighlight>[/color]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=red>$ibtxt{'1223'}</font>
                </td>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[list]</font>$ibtxt{'1224'}<br><font color=$fonthighlight>[*]</font>$ibtxt{'1216'}<br><font color=$fonthighlight>[/list]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=left valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><ul>$ibtxt{'1224'}<br><li>$ibtxt{'1216'}</ul></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><font color=$fonthighlight>[img]</font>http://www.domain.com/images/logo.gif<font color=$fonthighlight>[/img]</font>
                    </font>
                </td>
                    <td bgcolor="$miscbackone" align=left valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2><img src="$imagesurl/images/logo.gif" border=0></font>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;
    
} # end elsif 


elsif ($action eq "aim") {
$aimname=&cleaninput($aimname);  #пофиксили уязвимость 
$cleanboardname = $boardname;
$cleanboardname =~ s/ /\+/sg;

$output = qq~
    
    <html><head><title>$ibtxt{'1225'} $boardname</title></head>
    <body topmargin=10 leftmargin=0>
    <table width=95% cellpadding=0 cellspacing=1 border=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=6 cellspacing=1 border=0>
            <tr>
                <td bgcolor="$titlecolor" align=center valign=middle>
                    <font face="$font" color="$titlefontcolor" size=$dfontsize2><b>$boardname - $ibtxt{'1226'}</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="$miscbacktwo" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>
                    <a href="aim:goim?screenname=$aimname&message=$ibtxt{'1231'}+$ibtxt{'1232'}+$ibtxt{'0934'}+$cleanboardname">$ibtxt{'1227'} $aimname $ibtxt{'1228'}</a></font>
                </tr>
                <tr>
                    <td bgcolor="$miscbackone" align=center valign=middle>
                    <font face="$font" color="$fontcolormisc" size=$dfontsize2>
                    <a href="aim:addbuddy?screenname=$aimname">$ibtxt{'1229'} $aimname $ibtxt{'1230'}</a></font>
                </td>
                </tr>
            </table>
        </td></tr>
    </table>
    </body>
    </html>
    ~;


} # end aim

###########
print header('text/html; charset=windows-1251');
print $output;

exit;




