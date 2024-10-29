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
$CGI::HEADERS_ONCE = 1;                   # Kill redundant headers

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

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "announcements.cgi";


$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

for ('membername','password','announcementtitle','announcementpost','action','checked','number') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput($tp);
    ${$_} = $tp;
    }

$inmembername           = $membername;
$inpassword             = $password;
$inannouncementtitle    = $announcementtitle;
$inannouncementpost     = $announcementpost;


if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }

if ($inmembername eq "") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        }



	### Print Header for the page.

            print header('text/html; charset=windows-1251');

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
                        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0301'}
	                </tr>
                  </table>
	           <p>
	        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 border=0 width=100%>
	                ~;
	        
	### Startactions


	if ($action eq "delete") {

	        
	        if ($checked eq "yes") {
	        
	# Validate user
	        
	                &getmember("$inmembername");
	        
	                if ($membercode ne "ad") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0302'}."); }
	                elsif ($inpassword ne $password) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0303'}."); }
	        
	                # Get the announcement to delete
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen") or die "$ibtxt{'0324'}";
	                @announcements = <FILE>;
	                close(FILE);
	        
	                # Write it back minus the one to delete.
	        
	                $count = 0;
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, ">$filetoopen") or die "$ibtxt{'0324'}";
	                  flock (FILE, 2);
	                foreach $line (@announcements) {
	                chomp $line;
	                        if ($count ne $number) {
	                                print FILE "$line\n";
	                                }
	                        $count++;
	                        }
	                close(FILE);

                    &doend("$ibtxt{'0304'}");
                                   
	                exit;


	                } # end checked delete
	        
	                else {
	        
	                        &login("$thisprog?action=delete&number=$number&checked=yes");
	        
	                        } # end else
	                
	                  } # end action





	        elsif ($action eq "add") {

                            
	        
	                        # Present the form

	                        $output .= qq~
	                        <form action="$thisprog" method=post>
                            <input type=hidden name="action" value="addannouncement">
	                        <tr>
	                        <td bgcolor=$miscbacktwo colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'0305'}</b></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></a></td></tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0308'}</b></font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" size=60 maxlength=100></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0331'}</b><br>$ibtxt{'0309'}<p>$ibtxt{'0310'}</font></td>
	                        <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost"></textarea></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	                        <input type=Submit value=$ibtxt{'0039'} name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear"></form>
	                        </td></tr>
	                        ~;      
	        
	                        
	        } # end action






	        
	        elsif ($action eq "addannouncement") {
	                
	                $currenttime = time;
	                
	                # Validate user
	                
	                &getmember("$inmembername");
	        
	                if ($membercode ne "ad") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0303'}."); }
	                elsif ($inpassword ne $password) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0303'}."); }
	                
	                # Check for blanks.
	                
	                if ($inannouncementpost eq "") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0311'}."); }
	                if ($inannouncementtitle eq "") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0312'}"); }
	                
	                # Get the announcement file
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen");
	                @announcements = <FILE>;
	                close(FILE);
	        
	                # Write it back with the new announcement at the top
	        
	                $newline = "$inannouncementtitle|$currenttime|$inannouncementpost";
	                chomp $newline;
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, ">$filetoopen");
	                  flock(FILE, 2);
	                print FILE "$newline\n";
	                foreach $line (@announcements) {
	                        chomp $line;
	                        print FILE "$line\n";
	                        }
	                close(FILE);
	                
	                &doend("$ibtxt{'0313'}");
	                
	                } # end add announcement
	        
	        
	        
	        
	        
	        
	        
	        
	        
	        elsif ($action eq "edit") {

                    
	        
	                # Get the announcement file
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen") or die "$ibtxt{'0324'}";
	                @announcements = <FILE>;
	                close(FILE);
	        
	                # Get the announcement to edit
	        
	                $count = 0;
	                
	                foreach (@announcements) {
	                        if ($count eq $number) {
	                                ($announcementtitle, $notneeded, $announcementpost) = split(/\|/,$_);
	                                }
	                        $count++;
	                        }
	                
	                # Clean the text area
	                
	                $announcementpost =~ s/\<p\>/\n\n/g;
	                $announcementpost =~ s/\<br\>/\n/g;
	                
	                        # Present the form

	                        $output .= qq~
	                        <form action="$thisprog" method=post>
                            <input type=hidden name="action" value="doedit">
                            <input type=hidden name="number" value="$number">
	                        <tr>
	                        <td bgcolor=$miscbacktwo colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'0314'}</b></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></a></td></tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0308'}</b></font></td>
	                        <td bgcolor=$miscbackone valign=middle><input type=text name="announcementtitle" value="$announcementtitle"size=60 maxlength=100></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0331'}</b><br>$ibtxt{'0309'}.<p>$ibtxt{'0310'}.</font></td>
	                        <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=10 name="announcementpost">$announcementpost</textarea></td>
	                        </tr>
	                        <tr>
	                        <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
	                        <input type=Submit value=$ibtxt{'0039'} name=Submit onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear"></form>
	                        </td></tr>
	                        ~;      
	        
	                        
	        } # end action
	        








	        elsif ($action eq "doedit") {

	                $currenttime = time;
	                
	                # Make sure it's got all new lines converted
	                
	                # Validate user
	                
	                &getmember("$inmembername");
	        
	                if ($membercode ne "ad") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0303'}."); }
	                elsif ($inpassword ne $password) { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0332'}."); }
	                
	                # Check for blanks.
	                
	                if ($inannouncementpost eq "") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0311'}."); }
	                if ($inannouncementtitle eq "") { print header('text/html; charset=windows-1251'); &error("$ibtxt{'0301'}&$ibtxt{'0312'}"); }
	                
	                # Get the announcement file
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen") or die "$ibtxt{'0325'}";
	                @announcements = <FILE>;
	                close(FILE);
	        
	                # Write it back with the new announcement at the top
	        
	                $count = 0;
	                
	                $newline = "$inannouncementtitle|$currenttime|$inannouncementpost";
	                chomp $newline;
	        
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, ">$filetoopen") or die "$ibtxt{'0325'}";
	                  flock(FILE, 2);
	                foreach $line (@announcements) {
	                        chomp $line;
	                        if ($count eq $number) {
	                                print FILE "$newline\n";
	                                }
	                                else {
	                                        print FILE "$line\n";
	                                        }
	                        $count++;
	                        }
	                close(FILE);
	                
	                &doend("$ibtxt{'0315'}");
	                
	                exit;
	        
	                } # end edit announcement
	        
	        
	        
	        
	        
	        
	        

	        
	        else { # start last else
	        
	        
	                ### start displaying the announcements.
                    
                    
	                $filetoopen = "$ikondir" . "data/news.cgi";
                    $filetoopen = &stripMETA($filetoopen);
	                open(FILE, "$filetoopen");
	                @announcements = <FILE>;
	                close(FILE);
	        
	                $postcountcheck = 0;
	                
	                $totals = @announcements;
	                
	                if ($totals eq "0") { 
	                        $dateposted = time;             
	                        @announcements[0] = qq~$ibtxt{'0316'}|$dateposted|$ibtxt{'0317'} <a href="$thisprog?action=add"><img src="$imagesurl/images/a_add.gif" border=0"></a> $ibtxt{'0318'}~;
	                        }               
	                                        
	                
	                        foreach $line (@announcements) {
	                        

	                                ($title, $dateposted, $post) = split(/\|/, $line);
	        
	                                $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
	                                $dateposted = &dateformat("$dateposted");
	        
	                                $post = &ikoncode("$post");
	                                $post = &doemoticons("$post");
	                                
                                    $post =~ s/\:\)/<img src=\"$imagesurl\/emoticons\/smile.gif\" border=\"0\">/g;
                                    $post =~ s/\;\)/<img src=\"$imagesurl\/emoticons\/wink.gif\" border=\"0\">/g;
                                    $post =~ s/\:\(/<img src=\"$imagesurl\/emoticons\/sad.gif\" border=\"0\">/g;
                                    $post =~ s/\:\o/<img src=\"$imagesurl\/emoticons\/shocked.gif\" border=\"0\">/g;
	                                
	                                
	                                # Allow HTML
	                                
	                                $post =~ s/&lt\;/\</g;
	                                $post =~ s/&gt\;/\>/g;
	                                $post =~ s/&quot\;/\"/g;
	        
	                        if ($count eq "1") {
	                           $postbackcolor = "$postcolorone";
	                           $postfontcolor = "$postfontcolorone";
	                           $count++;
	                           }
	                            else {
	                                 $postbackcolor = "$postcolortwo";
	                                 $postfontcolor = "$postfontcolortwo";
	                                 $count = 1;
	                                 }
	                
	        
	                        $post = qq~<p><blockquote>$post</blockquote><p>~;
	        
	                        $adminadd = qq~<a href="$thisprog?action=add"><img src="$imagesurl/images/a_add.gif" border=0"></a>~;
	                        $admindelete = qq~<a href="$thisprog?action=delete&number=$postcountcheck"><img src="$imagesurl/images/a_delete.gif" border=0"></a>~;
	                        $adminedit = qq~<a href="$thisprog?action=edit&number=$postcountcheck"><img src="$imagesurl/images/a_edit.gif" border=0"></a>~;
	        
	                        $output .= qq~
	                        <tr>
	            <td bgcolor=$titlecolor align=center valign=top><font face="$font" color=$titlefontcolor size=$dfontsize3>
	            <b>&raquo; $title &laquo;</b>
	            </td>
	            </tr>~;
	                        
				&getmember("$inmembername");                           
				if ($membercode eq "ad") {                            
				$output .= qq~                           
				<tr>
				<td bgcolor=$postbackcolor align=left>$admindelete &nbsp; $adminedit &nbsp; $adminadd</td>                           	</tr>
				~;                          
				}                           

				$output .= qq~ 
	            <tr>
	            <td bgcolor="$postbackcolor" valign=top><font face="$font" color=$postfontcolor size=$dfontsize2>
	                     $post
	                     </td>
	                     </tr>
	                     
	                        <tr>
	                            <td bgcolor="$postbackcolor" valign=middle>
	                        <font face="$font" color=$postfontcolor size=$dfontsize2>$ibtxt{'0319'}: <b>$dateposted</b>
	                        </td>
	                        </font>
	                        </tr>
	                        
	                        ~;

	                        $postcountcheck++;
	        
	                        } # end foreach

	                    } # end last else



	                        $output .= qq~</table></td></tr></table>~;
                            
	                        &output(
                            -Title   => "$boardname - $ibtxt{'0301'}", 
                            -ToPrint => $output, 
                            -Version => $versionnumber 
                            );




	##############################################################
	### Sub route (login)

	        
	sub login {

	local($url) = @_;
	
    ($postto, $therest) = split(/\?/,$url);
    
    @pairs = split(/\&/,$therest);
    
    foreach (@pairs) {
        ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
        }
           
	    
   
	    $output .= qq~
	    <form action="$postto" method="post">$hiddenvars
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0320'}</font></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
	        ~;
	        
	 } # end routine        
	        
	sub doend {

    my $action_taken = shift;

    $relocurl = "$boardurl/$thisprog";    

    $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'0301'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'0321'}            <ul>
            <li><b>$action_taken</b>
            <li><a href="$relocurl">$ibtxt{'0322'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            &output(
            -Title   => "$boardname - $ibtxt{'0301'}", 
            -ToPrint => $output, 
            -Version => $versionnumber 
             );

}
