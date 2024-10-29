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
$CGI::HEADERS_ONCE = 1;                   # Make sure we only have 1 header

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

$thisprog = "register.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;


for ('inmembername','password','emailaddress','showemail','homepage','aolname','icqnumber',
     'location','interests','signature','timedifference','useravatar','action') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
    }

$helpurl = &helpfiles("–егистрация");
$helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;


&title;

    $output .= qq~
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
                <font face="$font" color=$fontcolormisc size=$dfontsize2>
	            &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	            <br>
                &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0105'}
            </td>
            </tr>
            <tr>
        <td valign=bottom align=right>&nbsp; $helpurl</td>
    </tr>
    </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    ~;

if ($action eq "addmember") { #start add member
        
        $membercode           = "me";
        $membertitle          = "$ibtxt{'0136'}";
        $numberofposts        = "0";
        $joineddate           = time;
        $lastpostdate         = "$ibtxt{'1816'}";
        $ipaddress            = $ENV{'REMOTE_ADDR'};


        # check against the ban lists

        $filetoopen = "$ikondir" . "data/banlist.cgi";

        open(FILE,"$filetoopen");
        @bannedmembers = <FILE>;
        close(FILE);
        

        foreach (@bannedmembers) {
            ($bannedname, $bannedemail, $bannedip) = split(/\|/,$_);
            chomp $bannedname;
            chomp $bannedemail;
            chomp $bannedip;
            if ($emailaddress =~ /^$bannedemail/) { $bannedmember = "yes"; }
            if ($inmembername eq "$bannedname") { $bannedmember = "yes"; }
            if ($ipaddress =~ /^$bannedip/) { $bannedmember = "yes"; }
            }
        

        if ($bannedmember eq "yes") {
print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'1903'}");
            }

# added by DimoN
if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {         
    my @datapassword = qw(A B C D E F G H J K L M N P Q R S T U V W Y Z a b c d e f g h j k l m n p q r s t u v w y z 0 12 3 4 5 6 7 8 9); 
    srand(time * (time *time));     
    for(1..7){$password .= $datapassword[rand(@datapassword)];}         
} 

    
#    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
#        $seed = int(rand 100000);
#        $password = crypt($seed, aun);
#        $password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
#        $password =~ s/\.//g;
#        $password =~ s/\|//g;
#        $password = substr($password, 0, 7);
#        }
        
    

    if ($interests) {
        $interests =~ s/\t//g;
        $interests =~ s/\r//g;
        $interests =~ s/  / /g;
        $interests =~ s/\n\n/\<p\>/g;
        $interests =~ s/\n/\<br\>/g;
        }
        
    
    
    if ($signature) {
        $signature =~ s/\t//g;
        $signature =~ s/\r//g;
        $signature =~ s/  / /g;
        $signature =~ s/\n\n//g;
        $signature =~ s/\n/\[br\]/g;
        }   

######check for bad words          

if ($membernamefilter eq "yes"){                        
$filetoopen = "$ikondir" . "data/badwords.cgi";            
open (FILE, "$filetoopen");            
$badwords = <FILE>;            
close (FILE);                     
if ($badwords) {                
@pairs = split(/\&/,$badwords);                
foreach (@pairs) {                    
($bad, $good) = split(/=/,$_);                    
if ($inmembername =~ /$bad/ig){                       
print header('text/html; charset=windows-1251'); &error("Registering&Please do not use profanity in your membername");                       
}                    
if ($signature =~ /$bad/ig){                       
print header('text/html; charset=windows-1251'); &error("Registering&Please do not use profanity in your signature");                       
}                    
}               
}            
}

### Throw an error if they have more than three sig lines.  
    
    
    @testsig = split(/\[br\]/,$signature);
    $siglines = @testsig;
    
    if (($siglines > "2") && (@testsig[3] ne "")) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'1857'}"); }
    

### make sure its a valid form


    if($inmembername eq "") { $blankfields = "yes"; }
    if($password eq "")     { $blankfields = "yes"; }
    if($emailaddress eq "") { $blankfields = "yes"; }

    if ($blankfields) {
        print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'1859'}");
        }
    if($inmembername =~ /_/) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'1904'}"); }
    
    $inmembername =~ y/ /_/;
    
    $_ = $inmembername;
         if ((m/\b[_]/) || (m/\W+/) || (m/_{2,}/) || (m/[_]\b/)) {
             print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'1905'}");
            }
    
    
    if($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&$ibtxt{'0906'}"); }


    
### check for an already in use member name

        &getmember("$inmembername");
        if ($userregistered ne "no") { $allowregister = "fail"; }
        my ($tempinusername) = $inmembername;
        chomp $tempinusername;
    opendir (DIR, $ikondir."members/"); 
	@foundreggedmember = grep { /^$tempinusername\.cgi/i } readdir(DIR); 
	closedir (DIR); 
	if (@foundreggedmember) { $allowregister = "fail"; } 

        
        if ($allowregister eq "fail") {
            print header('text/html; charset=windows-1251'); &error("$ibtxt{'1858'}&Error, $ibtxt{'1906'}");
            }

        
        
        $memberfiletitle = $inmembername;
        $memberfiletitle =~ y/ /_/;

        $filetomake = "$ikondir" . "members/$memberfiletitle.cgi";
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$inmembername|$password|$membertitle|$membercode|$numberofposts|$emailaddress|$showemail|$ipaddress|$homepage|$aolname|$icqnumber|$location|$interests|$joineddate|$lastpostdate|$signature|$timedifference|$privateforums|$useravatar|$misc1|$misc2|$misc3";
        close(FILE);

            $inmembername =~ y/_/ /;
            
            $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1912'} $inmembername</b></font></td></tr>
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
if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
    $output =~ s/$ibtxt{'1004'}\:/$ibtxt{'1908'}/;
    }
    
### Set the cookies
        
        $namecookie = cookie(-name    =>   "amembernamecookie",
                             -value   =>   "$inmembername",
                             -path    =>   "$cookiepath",
                             -expires =>   "+30d");
        $passcookie = cookie(-name    =>   "apasswordcookie",
                             -value   =>   "$inpassword",
                             -path    =>   "$cookiepath",
                             -expires =>   "+30d");
        
        
    
### Create a dummy file to foil snoopers, and to stop them gaining a list of the directory

    open (FILE, ">members/index.html");
    print FILE qq(
    <HTML><HEAD>
    <TITLE>401 $ibtxt{'1909'}</TITLE>
    </HEAD><BODY>
    <H1>$ibtxt{'1909'}</H1>
    $ibtxt{'1910'}<P>
    <HR>
    <ADDRESS>Apache/1.3.9 Server at $homeurl Port 80</ADDRESS>
    </BODY></HTML>);
    close (FILE);


### append boardstats.cgi

    require "$ikondir" . "data/boardstats.cgi";
        
    $filetomake = "$ikondir" . "data/boardstats.cgi";
        
    $totalmembers++;
        
    open(FILE, ">$filetomake");
      flock(FILE, 2);
    print FILE "\$lastregisteredmember = \"$inmembername\"\;\n";
    print FILE "\$totalmembers = \"$totalmembers\"\;\n";
    print FILE "\$totalthreads = \"$totalthreads\"\;\n";
    print FILE "\$totalposts = \"$totalposts\"\;\n";
    print FILE "\n1\;";
    close (FILE);

### Send the emails

if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {

                $passcookie = cookie(-name    =>   "apasswordcookie",
                                     -value   =>   "",
                                     -expires =>   "now");       
                
                
                $to = "$emailaddress";
                $from = "$homename <$adminemail_out>";
                $subject = "$ibtxt{'1911'} $boardname";

                
                $message .= "\n";
                $message .= "$homename\n";
                $message .= "$boardurl/$forumsummaryprog\n\n\n";
                $message .= "$ibtxt{'1913'}\n\n\n";
                $message .= "$ibtxt{'1863'}\n\n";
                $message .= "   $ibtxt{'0727'}  $inmembername\n";
                $message .= "   $ibtxt{'0728'}  $password\n\n\n";
                $message .= "$ibtxt{'1864'}\n\n";
                $message .= "$ibtxt{'1914'}\n";
                $message .= "$ibtxt{'1915'}\n";
                $message .= "$ibtxt{'1916'}\n\n";
                
                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
                
                } # end send password to member



if ($newusernotify eq "yes" && $emailfunctions ne "off") {

                $to = "$adminemail_in";
                $from = "$boardname <$adminemail_out>";
                $subject = "$ibtxt{'1917'}";

                $message = "";

                $message .= "$boardname\n";
                $message .= "$boardurl/$forumsummaryprog\n";
                $message .= "---------------------------------------------------------------------\n";
                $message .= "$ibtxt{'1918'}\n";
                $message .= "   $ibtxt{'0727'} $inmembername\n";
                $message .= "   $ibtxt{'0728'} $password\n";
                $message .= "   $ibtxt{'0804'}: $emailaddress\n";
                $message .= "   $ibtxt{'1920'}: $homepage\n";
                $message .= "   $ibtxt{'1921'}: $ipaddress\n";
                $message .= "---------------------------------------------------------------------\n";
                

                &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);
                
                } # end routine


} # end routine



elsif ($action eq "agreed") {

if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
    $requirepass = qq~
    <tr>
    <td bgcolor=$miscbackone colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1922'}</td>
    </tr>
    ~;
    }
    else {
        $requirepass = qq~
        <tr>
        <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b><br>$ibtxt{'1836'}</td>
        <td bgcolor=$miscbackone><input type=text size=20 name="password"></td>
        </tr>
        ~;
        }


### Avatar stuff


if ($avatars eq "on") {

        $dirtoopen = "$imagesdir" . "avatars";
        opendir (DIR, "$dirtoopen") or die "$ibtxt{'1923'} ($dirtoopen) $ibtxt{'1924'} \$imagesdir $ibtxt{'1925'} \&gt\; Set-Variables";
        @dirdata = readdir(DIR);
        closedir (DIR);

        @images = grep(/gif/,@dirdata);
        @images = sort @images;
        
        foreach (@images) {

            $cleanavatar =  $_;
            $cleanavatar =~ s/.gif//i;

            # Skip, if it's an admin/moderator only avatar

            if ($cleanavatar =~ /admin_/) { next; }
            
            if ($cleanavatar eq "noavatar") {            
	            $selecthtml .= qq~<option value="noavatar" selected>$cleanavatar</option>\n~;
                $currentface = "$cleanavatar";
                }
	            else {
                    $selecthtml .= qq~<option value="$cleanavatar">$cleanavatar</option>\n~;
                    }
                }

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



### Print the form


$output .= qq~

<form action="$boardurl/$thisprog" method=post name="creator">
<tr>
<td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1907'}</b><br>$ibtxt{'1926'}</td>
<td bgcolor=$miscbacktwo><input type=text size=20 maxlength="20" name="inmembername"></td>
</tr>
$requirepass
<tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1822'}</b><br>$ibtxt{'1837'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="emailaddress"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1838'}</b><br>
$ibtxt{'1839'}:</td>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><input name=\"showemail\" type=\"radio\" value=\"yes\" checked> $ibtxt{'0130'} &nbsp\; <input name=\"showemail\" type=\"radio\" value=\"no\"> $ibtxt{'0129'}</font></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1823'}</b><br>$ibtxt{'1840'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="homepage" value="http://"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1841'}</b><br>$ibtxt{'1842'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="aolname"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1825'}</b><br>$ibtxt{'1843'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="icqnumber"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1826'}</b><br>$ibtxt{'1844'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="location"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1845'}</b><br>
$ibtxt{'1927'} $basetimes.<br>$ibtxt{'1847'}</td>
<td bgcolor=$miscbackone><input type=text size=20 name="timedifference"></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1827'}</b><br>$ibtxt{'1848'}</td>
<td bgcolor=$miscbackone><textarea size=20 name="interests" cols="40" rows="5"></textarea></td>
</tr><tr>
<td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1849'}</b><br>$ibtxt{'1850'}
<br>$ibtxt{'1851'}<br>
$ibtxt{'1852'}</td>
<td bgcolor=$miscbackone><textarea size=20 name="signature" cols="40" rows="5"></textarea></td>
</tr>
$avatarhtml
<tr>
<td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value=$ibtxt{'0039'} name=submit></td>
<input type=hidden name=action value=addmember></form></tr></table></td></tr></table>

~;

} # end agree


else { # show register agree form

    
    $filetoopen = "$ikondir" . "data/register.dat";

    open(FILE,$filetoopen) or die "$ibtxt{'1928'}";
    @filedata = <FILE>; close(FILE);
    foreach (@filedata) { $tempoutput .= $_; }
    
    $output .= qq~
    <form action="$thisprog" method="post">
    <input name="action" type="hidden" value="agreed">
    <tr>
    <td bgcolor=$miscbacktwo align=center><font face="$font" color=$fontcolormisc size=$dfontsize3>
    <b>$ibtxt{'1929'}</b>
    </td>
    </tr>
    <td bgcolor=$miscbackone align=left><font face="$font" color=$fontcolormisc size=$dfontsize2>

     $tempoutput
        
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center>
    <center><input type="submit" value="$ibtxt{'1930'}"></center>
    </td></tr></table>
    </form>
    </td></tr></table>
    ~;


} # end elseform

    print header(-cookie=>[$namecookie, $passcookie]);    
    
    &output(
    -Title   => $boardname, 
    -ToPrint => $output, 
    -Version => $versionnumber 
    );

