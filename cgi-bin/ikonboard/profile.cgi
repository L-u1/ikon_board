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
require "ikonmail.lib";      # Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                    # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "profile.cgi";

$query = new CGI;

&checkVALIDITY;
$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ y/$thisprog//;

$action              = $query -> param('action');
$inmember            = $query -> param('member');
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$oldpassword         = $query -> param("oldpassword");
$passmembername      = $query -> param("passmembername");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");


    if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
       
 if (($inmembername eq "")||($inmembername eq "Guest")) 
    { $inmembername = "Guest"; }
    else {
        &getmember("$inmembername");
        }
    # Print the page title

    print header(-cookie=>[$namecookie, $passcookie]);
 
    &title;
    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
                <font face="$font" color=$fontcolormisc size=$dfontsize2>
	             &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	             <br>
                 &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0111'}
            </td>
        </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    ~;





    my %Mode = ( 
    'show'                 =>    \&showprofile,
    'process'              =>    \&savemodify, 
    'lostpassword'         =>    \&lostpasswordform,        
    'lostpass'             =>    \&lostpasswordform,
    'sendpassword'         =>    \&sendpassword, 
    'modify'               =>    \&modify,
    );



    if($Mode{$action}) { 
        $Mode{$action}->();
        }
        else{

        $inmembername =~ s/\_/ /g;
        $output .= qq~
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="modify">
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1801'}</b></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
        <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
        <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
        ~;

        } # end else
    
        
        &output(
	           -Title   => $boardname, 
	           -ToPrint => $output, 
	           -Version => $versionnumber 
	            );








	# lost password routine

	sub lostpasswordform {

	    &helpfiles("Забытый_пароль");
	    
	    $output =~ s/\&nbsp\;$ibtxt{'0111'}/\&nbsp\;$ibtxt{'0112'}/g;
	    
	    $output .= qq~
	    <p><form action="$thisprog" method="post">
	    <input type=hidden name="action" value="sendpassword">
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1802'}</b></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</td>
	    <td bgcolor=$miscbackone><input type=text name="passmembername"> &nbsp; $helpurl</td></tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name=submit value=$ibtxt{'0039'}>
	    </form></td></tr></table></td></tr></table>
	    ~;

	} # end lost password form.

	sub sendpassword {

	
	&gettopicmember("$passmembername");

	if ($membercode eq "ad") { &blocked; }
	elsif ($userregistered ne "no") { # start emailing functions

	                $message .= "\n";
	                $message .= "$boardname\n";
	                $message .= "$homeurl\n\n";
	                $message .= "$ibtxt{'1803'}\n\n";
	                $message .= "$password\n\n\n";
	                $message .= "$ibtxt{'1804'}\n";
	                $message .= "$ibtxt{'1805'}\n";
	                $message .= "$ibtxt{'1806'}\n\n";

	                $to = "$emailaddress";
	                $from = "$homename <$adminemail_out>";
	                $subject = "$ibtxt{'0112'}";

	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );
	                
	                $output =~ s/$ibtxt{'1812'}<\/a> \/ Profile/Home<\/a> \/ $ibtxt{'1808'}/g;	                
	                $output .= qq~
	                <tr>
	                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'1809'} $passmembername!</b></font></td></tr>
	                <tr>
	                <td bgcolor=$miscbackone align=center><font face="$font" color=$fontcolormisc size=$dfontsize2>
	                $ibtxt{'1810'}
	                </td></tr></table></td></tr></table>
	                 ~;
	               
	                } # end user registered.
	                
	                else {
	                    &error("$ibtxt{'1811'}&$ibtxt{'1102'}");
	                    }
	} # end routine.



	################ show profile subroutine

	sub showprofile {
    &whosonline("$inmembername|$ibtxt{'1813'}|$ibtxt{'1602'}");
	$inmember =~ s/\_/ /isg;

	&getmember("$inmember");

	    if ($showemail ne "yes") { $emailaddress = "Private"; }
	        else { $emailaddress = qq~<a href="mailto:$emailaddress">$emailaddress</a>~; }
	    if ($aolname eq "") { $aolname = "$ibtxt{'1602'}"; }
	    if ($icqnumber eq "") { $icqnumber = "$ibtxt{'1602'}"; $icqlogo = ""; } else { $icqlogo = qq~<img src="http://wwp.icq.com/scripts/online.dll?icq=$icqnumber&img=7" border=0>~; }
	    if ($membercode eq "banned") { $membertitle = "$ibtxt{'3010'}"; }
	    if ($homepage eq "http://") { $homepage = "$ibtxt{'1602'}"; } else { $homepage = qq~<a href="$homepage" target="_blank">$homepage</a>~; }
	    
	    $joineddate = &longdate($joineddate + ($timedifferencevalue*3600) + ($timezone*3600));
	    
	    ## Sort last post, and where
	    
	    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
	    
	    if ($postdate ne "$ibtxt{'1816'}") {
	        $postdate = &longdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
	        $lastpostdetails = qq~$ibtxt{'1815'} <a href="$posturl">$posttopic</a> $ibtxt{'1119'} $postdate~;
	        }
	        else {
	            $lastpostdetails = "$ibtxt{'1816'}";
	            }
	    $inmember =~ y! !_!; &set_up_guest() unless (-e $ikondir . 'members/'.$inmember.'.cgi');

# Убираем профиль несуществующего пользователя
$filetoopen = "$ikondir" . "members/$inmember.cgi";  
unless (-e $filetoopen) { &error("Пользователь не найден&Пользователь $inmember не зарегистрирован на нашей конференции"); }
# Убрали	    	    
	    $output .= qq~
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'1817'} <font color=$fonthighlight>$inmember</b></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1818'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$joineddate</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1819'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$membertitle</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0013'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$lastpostdetails</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0212'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$numberofposts</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1822'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$emailaddress</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1823'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$homepage</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1824'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$aolname</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1825'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$icqnumber</font>&nbsp; $icqlogo</td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1826'}</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$location</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1827'}</b></font></td>
	    <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize1>$interests</font></td></tr>
	    </table></td></tr></table>
	    ~;
	    
    } # end showprofile


    ############################## start profile modification

	sub modify {

	$helpurl = &helpfiles("Профиль");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

	&getmember("$inmembername");

	if ($userregistered eq "no") { &error("$ibtxt{'1828'}&$ibtxt{'1829'}"); }
	if ($inpassword ne $password) { &error("$ibtxt{'1828'}&$ibtxt{'1830'}"); }

	if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
	    $newpassneeded = "<br>$ibtxt{'1831'}";
	    }

    ### Avatar stuff


if ($avatars eq "on") {

        $dirtoopen = "$imagesdir" . "avatars";
        opendir (DIR, "$dirtoopen") or die "$ibtxt{'1832'} ($dirtoopen)"; 
        @dirdata = readdir(DIR);
        closedir (DIR);

        @images = grep(/gif/,@dirdata);
        @images = sort @images;

        foreach (@images) {

            $cleanavatar =  $_;
            $cleanavatar =~ s/.gif//i;

            # Skip, if it's an admin/moderator only avatar

            if (($cleanavatar =~ /admin_/) && ($membercode eq "me")) { next; }
            
            if ($cleanavatar eq "$useravatar") {            
	            $selecthtml .= qq~<option value="$cleanavatar" selected>$cleanavatar</option>\n~;
                $currentface = "$cleanavatar";
                }
                elsif (($cleanavatar eq "noavatar") && (!$useravatar)) {
                    $selecthtml .= qq~<option value="noavatar" selected>noavatar</option>\n~;
                    $currentface = "$cleanavatar";
                    }  
	                else {
                        $selecthtml .= qq~<option value="$cleanavatar">$cleanavatar</option>\n~;
                        }
                    } # end foreach

              

            $avatarhtml = qq~
            <script language="javascript">
            function showimage()
            {
            //alert("$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif");
                document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";
                }
            </script>
            <tr>
                <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1833'}</b><br>$ibtxt{'1834'}</td>
                <td bgcolor=$miscbackone>
                    <select name="useravatar" size=6 onChange="showimage()">
                    $selecthtml
                    </select>
                    <img src="$imagesurl/avatars/$currentface.gif" name="useravatars" width="64" height="64" border=0 hspace=15>
                </td>
            </tr>
            ~;
            } # end avatar if



	$signature =~ s/\[br\]/\n/isg;
    $interests =~ s/\<br>/\n/isg;
$tempoutput = qq~<input name=\"newshowemail\" type=\"radio\" value=\"yes\"> $ibtxt{'0130'} &nbsp\; <input name=\"newshowemail\" type=\"radio\" value=\"no\"> $ibtxt{'0129'}~;  $tempoutput =~ s/value=\"$showemail\"/value=\"$showemail\" checked/; 
	$output .= qq~

	<form action="$thisprog" method=post name="creator">
	<input type=hidden name="action" value="process">
    <input type=hidden name="oldpassword" value="$inpassword">
	<tr>
	<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'1835'} <font color=$fonthighlight>$inmembername</b></font></td></tr>
	<tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b><br>$ibtxt{'1836'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newpassword" value="$inpassword">&nbsp; $helpurl</td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1822'}</b><br>$ibtxt{'1837'}$newpassneeded</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newemailaddress" value="$emailaddress"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1838'}</b><br>$ibtxt{'1839'}:</td>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1>$tempoutput</font></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1823'}</b><br>$ibtxt{'1840'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newhomepage" value="$homepage"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1841'}</b><br>$ibtxt{'1842'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newaolname" value="$aolname"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1825'}</b><br>$ibtxt{'1843'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newicqnumber" value="$icqnumber"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1826'}</b><br>$ibtxt{'1844'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newlocation" value="$location"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1845'}</b><br>
	$ibtxt{'1927'} $basetimes.<br>$ibtxt{'1847'}</td>
	<td bgcolor=$miscbackone><input type=text size=20 name="newtimedifference" value="$timedifference"></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1827'}</b><br>$ibtxt{'1848'}</td>
	<td bgcolor=$miscbackone><textarea size=20 name="newinterests" cols="40" rows="5">$interests</textarea></td>
	</tr><tr>
	<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1849'}</b><br>$ibtxt{'1850'}
	<br>$ibtxt{'1851'}<br>
	$ibtxt{'1852'}</td>
	<td bgcolor=$miscbackone><textarea size=20 name="newsignature" cols="40" rows="5">$signature</textarea></td>
	</tr>
    $avatarhtml
    <tr>
	<td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value=$ibtxt{'0039'} name=submit></td>
	<input type=hidden name="membername" value="$inmembername"></form></tr></table></td></tr></table>

	~;

	} # end modify routine


	############################## save profile modification

	sub savemodify {

        &getmember("$inmembername");

	    if ("$userregistered" eq "no") { &error("$ibtxt{'1828'}&$ibtxt{'1829'}"); }
	    if ("$oldpassword" ne "$password") { &error("$ibtxt{'1828'}&$ibtxt{'1830'}"); }


	    $newpassword            = $query -> param('newpassword');
	    $newshowemail           = $query -> param('newshowemail');
	    $newhomepage            = $query -> param('newhomepage');
	    $newaolname             = $query -> param('newaolname');
	    $newicqnumber           = $query -> param('newicqnumber');
	    $newlocation            = $query -> param('newlocation');
	    $newinterests           = $query -> param('newinterests');
	    $newtimedifference      = $query -> param('newtimedifference');
	    $newemailaddress        = $query -> param('newemailaddress');
        $newsignature           = $query -> param('newsignature');
        $inuseravatar           = $query -> param('useravatar');
        
        $newsignature           = &unHTML("$newsignature");
        $inuseravatar           = &cleaninput("$inuseravatar");
	    $newpassword            = &cleanarea("$newpassword");
	    $newshowemail           = &cleanarea("$newshowemail");
	    $newhomepage            = &cleanarea("$newhomepage");
	    $newaolname             = &cleanarea("$newaolname");
	    $newicqnumber           = &cleanarea("$newicqnumber");
	    $newlocation            = &cleanarea("$newlocation");
	    $newinterests           = &cleanarea("$newinterests");
	    $newtimedifference      = &cleanarea("$newtimedifference");
	    $newemailaddress        = &cleanarea("$newemailaddress");

        if ($newsignature) {
        
    ####Check for bad words in signature            
	if ($membernamefilter eq "yes"){                           
	$filetoopen = "$ikondir" . "data/badwords.cgi";               
	open (FILE, "$filetoopen");               
	$badwords = <FILE>;               
	close (FILE);                        
	if ($badwords) {                   
	@pairs = split(/\&/,$badwords);                   
	foreach (@pairs) {                       
	($bad, $good) = split(/=/,$_);                       
	if ($newsignature =~ /$bad/ig){                          
	&error("Modifying Profile&Please do not use profanity in your signature");                          
	}                       
		}                  
			}               
				}
        
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\n\n//g;
        $newsignature =~ s/\n/\[br\]/g;
        }   

        
            
	    # make sure its a valid form
	    
	    @testsig = split(/\[br\]/,$newsignature);
	    $siglines = @testsig;
	    
	    if (($siglines > "2") && (@testsig[3] ne "")) { &error("$ibtxt{'1856'}&$ibtxt{'1857'}"); }
	    

	    if (($newpassword eq "") && ($passwordverification ne "yes") && ($emailfunctions ne "on")) { $blankfields = "yes"; }
	    elsif ($newemailaddress eq "") { $blankfields = "yes"; }

	    if ($blankfields) {
	        &error("$ibtxt{'1858'}&$ibtxt{'1859'}");
	        }

	    # Sort out new cookies
        
        $namecookie = cookie(-name    =>   "amembernamecookie",
                             -value   =>   "$inmembername",
                             -path    =>   "$cookiepath",
                             -expires =>   "+30d");
        $passcookie = cookie(-name    =>   "apasswordcookie",
                             -value   =>   "$inpassword",
                             -path    =>   "$cookiepath",
                             -expires =>   "+30d");
        
        

	    
	    if($newemailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("$ibtxt{'1858'}&$ibtxt{'0906'}"); }

	    &getmember("$inmembername");
	    
	    if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	        
	        $seed = int(rand 100000);
	        $password = crypt($seed, aun);
	        $password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	        $password =~ s/\.//g;
            $password =~ s/\|//g;
	        $newpassword = substr($password, 0, 7);
	        
            # Sort out new cookies
        
            $passcookie = cookie(-name    =>   "apasswordcookie",
                                 -value   =>   "",
                                 -path    =>   "$cookiepath",
                                 -expires =>   "-1d");
        
	        ### send the email
	    
	    
	                $to = "$newemailaddress";
	                $from = "$homename <$adminemail_out>";
	                $subject = "$ibtxt{'1861'} $boardname";

	                
	                $message .= "\n";
	                $message .= "$homename\n";
	                $message .= "$boardurl/$forumsummaryprog\n\n\n";
	                $message .= "$ibtxt{'1862'}\n\n\n";
	                $message .= "$ibtxt{'1863'}\n\n";
	                $message .= "   $ibtxt{'0727'}  $inmembername\n";
	                $message .= "   $ibtxt{'0728'}  $newpassword\n\n\n";
	                $message .= "$ibtxt{'1864'}\n\n";

	                
	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );
	                
	                

	        } # end new password request
	    

	        $memberfiletitle = $inmembername;
	        $memberfiletitle =~ s/ /\_/isg;

	        $filetomake = "$ikondir" . "members/$memberfiletitle.cgi";
	        open(FILE, ">$filetomake");
	          flock(FILE, 2);
	        print FILE "$inmembername|$newpassword|$membertitle|$membercode|$numberofposts|$newemailaddress|$newshowemail|$ipaddress|$newhomepage|$newaolname|$newicqnumber|$newlocation|$newinterests|$joineddate|$lastpostdate|$newsignature|$newtimedifference|$privateforums|$inuseravatar|$misc1|$misc2|$misc3";
	        close(FILE);

	            $output .= qq~
	            <tr>
	            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1865'}</b></font></td></tr>
	            <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
	            $ibtxt{'1004'}:
	            <ul>
	            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
	            </ul>
	            </tr>
	            </td>
	            </table></td></tr></table>
	            ~;
	            
	            if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	            $output =~ s/$ibtxt{'1004'}\:/$ibtxt{'1866'}/g;
	            }
	    
	} # end save details.

	########### Lets stop people trying to get the Admin's password.

	sub blocked {

	    if ($inmembername eq "") { $inusername = "$ibtxt{'0043'}"; }
	    $ipaddress = $ENV{'REMOTE_ADDR'};
	    $inmembername =~ s/\_/ /g;
	    
	    
	    $output .= qq~
	    <p>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b><font color=$fonthighlight>$ibtxt{'1868'}</b></font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1>
	    <b>$ibtxt{'1869'}</b><p>
	    $ibtxt{'1870'}<br>
	    $ipaddress &nbsp; $ibtxt{'1871'}<br>
	    $ibtxt{'1872'} $ENV{'HTTP_USER_AGENT'}<p>
	    $ibtxt{'1873'}<p><p>
	    --$ibtxt{'1874'}
	    </td></tr></table></td></tr></table>
	    ~;
	    
	                $message .= "\n";
	                $message .= "$boardname\n";
	                $message .= "$homeurl\n\n";
	                $message .= "-----------------------------------------------------\n";
	                $message .= "$ibtxt{'1875'}\n\n";
	                $message .= "$ibtxt{'1876'}\n";
	                $message .= "\n";
	                $message .= "$ibtxt{'1877'}\n";
	                $message .= "$ibtxt{'1878'}\n";
	                $message .= "$ibtxt{'1879'}\n";
	                $message .= "$ibtxt{'1880'}\n";
	                $message .= "$ibtxt{'1881'}\n";
	                $message .= "------------------------------------------------------\n";
	                $message .= "$ibtxt{'1882'} $inmembername\n";
	                $message .= "$ibtxt{'1883'}   $ipaddress\n";
	                $message .= "------------------------------------------------------\n";
	                $to = "$adminemail_in";
	                $from = "$homename <$adminemail_out>";
	                $subject = "$ibtxt{'1884'}\! $ibtxt{'1885'}";


	                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );
	                
	                $output =~ s/$ibtxt{'1812'}<\/a> \/ Profile/Home<\/a> \/ $ibtxt{'1884'}/g;   

	                            &output(
	                            -Title   => $boardname, 
	                            -ToPrint => $output, 
	                            -Version => $versionnumber 
	                            );
	    }

