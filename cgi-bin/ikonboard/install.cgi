#!/usr/bin/perl

#############################################################
#
# >>>>>> SET UP ASSISTANT
#
#
# Ikonboard v2.1
# Copyright 2000 Ikonboard.com - All Rights Reserved
# Ikondiscussion is a trademark of Ikonboard.com
#
# Software Distributed by: Ikonboard.com
# Visit us online at http://www.ikonboard.com
# Email us on boards@ikonboard.com
#
# All files written by Matthew Mecham
#############################################################
use CGI::Carp "fatalsToBrowser";
use CGI qw(:standard);

$query = new CGI;
@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam =~ s/\@/\\\@/g;
		      ${$param} = $theparam;
        if ($param ne "action") {
            $printme .= "\$" . "$param = \"$theparam\"\;\n";
            }
	}
$stylesheet =<<__end_of_sheet__;
<!--
textarea, input {   FONT-FAMILY:verdana,arial;color:#000000; FONT-SIZE: 14px; background-color:#FFFFFF; width:500px  }
SELECT, option {   FONT-FAMILY:verdana,arial;color:#000000; FONT-SIZE: 14px; background-color:#eeeeee }

-->
__end_of_sheet__

$thisprog = "install.cgi"; $|=1; 
if ($action ne "final_step" || !$action) { print header('text/html; charset=windows-1251'); print start_html(-title=>"�������� ��������� Ikonboard", -bgcolor=>"#EEEEEE", -style=>{-code=>$stylesheet}); }

if ($action eq "step_two") {

$endprint = "1\;\n";

$errorflag = 0;

        $filetomake = "$ikondir" . "data/boardinfo.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2);
        print FILE "$printme";
        print FILE "\$dfontsize1 = \"1\"\;\n";
       	print FILE "\$dfontsize2 = \"2\"\;\n";
       	print FILE "\$dfontsize3 = \"3\"\;\n";
       	print FILE "\$dfontsize4 = \"4\"\;\n";
        print FILE "\$char_in_topic = \"80\"\;\n";
        print FILE "\$char_locat_in_topic = \"18\"\;\n";
        print FILE $endprint;
        close(FILE);
        
        
        if (-e $filetomake && -w $filetomake) {
            $saved_variables = qq(<font face="verdana" size="3" color="#0000FF">��� ��������� �������� ��������� �������� � $ikondir data/boardinfo.cgi.</font>);
            }
            else {
                $saved_variables = qq(<font face="verdana" size="3" color="#FF0000">��������. � �� ���� ��������� ��������.
                                      �� ������� $ikondir/data ���� � ����� 'data'. ��� �����?
                                      ���� ��� ���, ��������� CHMOD �� ����� 'data' � �������������� ������� �����
                                      ��� �������� � ����� � ����������);
                                       $errorflag = "1";
                }
      
        $filetocheck = "$ikondir" . "ikonboard.cgi";
        if (-e $filetocheck) {
            $found_cgi = qq(<font face="verdana" size="2" color="#0000FF">��������� - ������ $filetocheck</font>);
            }
            else {
                $errorflag = "1"; $found_cgi = qq(<font face="verdana" size="2" color="#FF0000">����������� - �� ������ $filetocheck, �������������� ������� ����� � ���������.</font>);
                }
          
        $dirtocheck = "$ikondir" . "data";
        if (-d "$dirtocheck") {
            $datadir = "found"; 
            $makefile = "$ikondir" . "data/test.txt";
            open (TEST, ">$makefile") or $datawritable = "����� data �� ��������, ��������� chmod";
            print TEST "-";
            close (TEST);
            $datawritable = "����� 'data' <b>��������</b>" if (!$datawritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $datadir = "<b>�� �������</b>"; }

        $dirtocheck = "$ikondir" . "help";
        if (-d "$dirtocheck") {
            $helpdir = "found"; 
            $makefile = "$ikondir" . "help/test.txt";
            open (TEST, ">$makefile") or $helpwritable = "����� 'help' �� ��������, ��������� chmod";
            print TEST "-";
            close (TEST);
            $helpwritable = "����� 'help' <b>��������</b>" if (!$helpwritable);
            unlink "$makefile";
            } else { $helpdir = "<b>�� �������</b>"; }

        $dirtocheck = "$ikondir" . "members";
        if (-d "$dirtocheck") {
            $membersdir = "found"; 
            $makefile = "$ikondir" . "members/test.txt";
            open (TEST, ">$makefile") or $memberswritable = "����� 'members' �� ��������, ��������� chmod";
            print TEST "-";
            close (TEST);
            $memberswritable = "����� 'members' <b>��������</b>" if (!$memberswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $membersdir = "<b>�� �������</b>"; }

        $dirtocheck = "$ikondir" . "messages";
        if (-d "$dirtocheck") {
            $messagesdir = "found"; 
            $makefile = "$ikondir" . "messages/test.txt";
            open (TEST, ">$makefile") or $messageswritable = "����� 'messages' �� ��������, ��������� chmod";
            print TEST "-";
            close (TEST);
            $messageswritable = "����� 'messages' <b>��������</b>" if (!$messageswritable);
            unlink "$makefile";
            } else { $errorflag = "1"; $messagesdir = "<b>�� �������</b>"; }


        $filetocheck = "$imagesdir" . "images/logo.gif";
        if (-e $filetocheck) {
            $found_image = qq(<font face="verdana" size="2" color="#0000FF">Correct</font>);
            }
            else {
                $errorflag = "1"; $found_image = qq(<font face="verdana" size="2" color="#FF0000">�����������, �������������� ������� ����� � ���������.</font>);
                }
          
        $dirtocheck = "$imagesdir" . "images";
        if (-d "$dirtocheck") { $images_dir = "�������"; } else { $errorflag = "1"; $images_dir = "<b>�� �������</b>"; } 

        $dirtocheck = "$imagesdir" . "emoticons";
        if (-d "$dirtocheck") { $emoticonsdir = "�������"; } else { $errorflag = "1"; $emoticonsdir = "<b>�� �������</b>"; }

        $dirtocheck = "$imagesdir" . "avatars";
        if (-d "$dirtocheck") { $avatarsdir = "�������"; } else { $errorflag = "1"; $avatarsdir = "<b>�� �������</b>"; }


        @progs_to_search = ('admincenter.cgi', 'announcements.cgi', 'checkboard.cgi', 'forumoptions.cgi', 'forums.cgi', 'help.cgi', 'ikon.lib', 'ikonadmin.lib',
                            'ikonboard.cgi', 'ikonfriend.cgi', 'ikonmail.lib', 'loginout.cgi', 'messenger.cgi', 'misc.cgi', 'newposts.cgi', 'post.cgi',
                            'postings.cgi', 'printpage.cgi', 'profile.cgi', 'privacy.cgi', 'register.cgi', 'search.cgi', 'setbadwords.cgi', 'setforums.cgi', 'setmembers.cgi',
                            'setmembertitles.cgi', 'setstyles.cgi', 'settemplate.cgi', 'setvariables.cgi', 'topic.cgi', 'viewip.cgi', 'data/progs.cgi', 'data/styles.cgi');

        
		print qq(
		    <font size="5" face="Trebuchet MS" color="#000000">
		    <h1>�������� ��������� Ikonboard</b></font></h1>
		    <hr noshade size=1 color="#000000">
		    <br>
		    <font face="verdana" size="3" color="#000000">
		    <b>����� ���������� � ��������� Ikonboard!</b>
		    <br><br><font size=2>
		    <b>��� ���:</b> ���������� �� ���� ��������. ����� ���������� ������� ���������.<br>���� �� �������� ������ � ����� �������, ��������� ������� ����������� ����� � ������ �� ����� ������� � ������������ ��������� chmod.</font><br>

		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>��������� �� ��������� �������� ������ ?</b></font>
		    <br>
		    $saved_variables
		    <br>
		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>����� �����</b></font>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    �������� (*.cgi) �� ������� ����: $ikondir - $found_cgi
		    <br><br>
		    -- �������� $ikondir data - $datadir - $datawritable<br>
		    -- �������� $ikondir help - $helpdir - $helpwritable<br>
		    -- �������� $ikondir messages - $messagesdir - $messageswritable<br>
		    -- �������� $ikondir members - $membersdir - $memberswritable<br>
		    <br>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    ��� non-cgi (images) �� ������� ����: $imagesdir - $found_image
		    <br><br>
		    -- �������� $imagesdir images - $images_dir<br>
		    -- �������� $imagesdir emoticons - $emoticonsdir<br>
		    -- �������� $imagesdir avatars - $avatarsdir<br>

		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>����� URL</b></font>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    URL �������� �� �������: $imagesurl
		    <br>
		    <br>
		    -- �������� $imagesurl/images/announce.gif - <img src="$imagesurl/images/announce.gif" border=0><br>
		    -- �������� $imagesurl/emoticons/smile.gif - <img src="$imagesurl/emoticons/smile.gif" border=0><br>
		    -- �������� $imagesurl/avatars/noavatar.gif - <img src="$imagesurl/avatars/noavatar.gif" border=0><br><br>
		    ���� � ��� ��������� � ����������, ��������� $html_url URL ����� ��������� � ��� ������������, ����� ���������,
		    ��� ��� �������� ��������� �� ������ � ������ BINARY.
		    );
		    if ($errorflag eq "1") { print qq(<br><br><font color="#FF0000" size="3"> �������� ��������� Ikonboard ����� ������ � �� ����� ����������. ��������� � ������������� ��� ������.); print end_html; exit; }

		    
		    print qq(
		    <hr noshade size=1 color="#000000">
		    <font face="verdana" size="3" color="#0000FF">
		    <b>�������� ����������� ������</b></font>
		    <br>
		    <br>
		    <font face="verdana" size="2" color="#000000">
		    �������� ��������� Ikonboard ������ ��������� *.cgi ����� ��� �����������, ��� ��� ��� ��������� �� ������ � ������ ASCII
		    <br><br>);

		    foreach (@progs_to_search) {

		        $filetotest = "$ikondir" . "$_";
		        if (-e $filetotest) {
		            open (TEST, "$filetotest");
		            @testfile = <TEST>;
			        close (TEST);
			        if (grep(/\r/, @testfile) && $^O ne "MSWin32") {
				        print "������ $_ ������� �������� � ������ BINARY. ������������� � ASCII<br>";
		                }
		                else { print "������ $_ - �������� ��<br>"; }
		            }
		            else { print "<b>�� ������ $_ ! - �� ��������?</b><br>"; }

		            } # end foreach

		    print qq(
		        <br><br>
		        <hr noshade size=1 color="#000000">
		        <font face="verdana" size="3" color="#0000FF">
		        <b>����� ��������</b></font>
		        <br>
		        <br>
		        <font face="verdana" size="2" color="#000000">
		        �������� ��������� Ikonboard �������� ��������. ���� ��������� ����� ������, ��������� � ������������� ��� ������.
		        <br>�� ������ � ����� ����� �������� �������� �������� � ������ ���������� Ikonboard.
		        <br><br>
		        ���� �� �� ������� � ���-����, ��������� � <a href="http://www.ikonboard.com/cgi-bin/ikonboard.cgi"><b>����� ���������</b></a>
		        <br><br><i>����� �������</i>
		        <br><br>
		        <hr noshade size=1 color="#000000">
		        <font face="verdana" size="3" color="#0000FF">
		        <b>��� ������?</b></font>
		        <br>
		        <br>
		        <font face="verdana" size="3" color="#000000">
		        <b>���� �� ������ ���������� Ikonboard � ������� ������, <a href="admincenter.cgi?action=remove">����� � ����� ���������� ������!</a></b>.
		        <font size=2><br>��� ������ ������ ���� ���� ����� ���˨� � ������ ������� ��� ������ �� �������� ������� � ����� ����������.<br>
		        ����� ���������� �� ����������, ���� �� �������� install.cgi �� ����� �������! ���� �������������� �������� �� �����������, ������� install.cgi �������, ����� FTP.
		        <br><br>
		        <font size="3"><b>���� ��� ������ ��������� <a href="$thisprog?action=step_three">��������� � ���� ���!</a></b></font>
		        <br><br><br><br><br>
		        );

                }


elsif ($action eq "step_three") {

    print qq(
    <font size="5" face="Trebuchet MS" color="#000000">
    <h1>�������� ��������� Ikonboard</b></font></h1>
    <hr noshade size=1 color="#000000">
     <br>
    <font face="verdana" size="3" color="#FF0000">
    <b>�� ��� �������� �����?</b>
    <br><br>
    <font face="verdana" size="2" color="#000000">
    <b>���� �� ������ ���������� Ikonboard � ������� ������, <a href="admincenter.cgi?action=remove">����� � ����� ���������� ������!</a></b>.
    <br><br>���� �� ����������� ���������, ���������� ����� ����� <b>����� ��������</b>! 
    <hr noshade size=1 color="#000000">
    <br><br><font size=2>
    <b>��� ���:</b><br>
    ��������� ���������. ����� ��� ����� ����� ���������, �� ������ ������ ������ ������� � ����� ����������
    ��� ��������� ������ � ���������� ������ ���� �������.
    <br>
    <hr noshade size=1 color="#000000">
    <br>
    <font face="verdana" size="3" color="#0000FF">
    <b>����������������� ��� �������������.</b></font>
    <br><br>
    <font face="verdana" size="2" color="#000000">
    ������ �� ������ ������������������ ��� �������������. ��� �������� ��� ������� � ����� ����������.</font>
    <br><br>
    <form action="$thisprog" method="post">
    <input type="hidden" name="action" value="final_step">
    <font face="verdana" size="2" color="#000000">
    �������� ���� ���<br>
    <input type="text" name="membername">
    <br><br>
    �������� ������<br>
    <input type="password" name="password_one">
    <br><br>
    ��������� ���� ������<br>
    <input type="password" name="password_two">
    <br><br>
    <input type="submit" value="submit">
    </form>
    <hr noshade size=1 color="#000000">
    <br>
    <b>������ ��������� ��� ������.</b>
    <br><br>);

    } # end step 3

elsif ($action eq "final_step") {

		$namecookie = cookie(-name    =>   "adminname",
		                     -value   =>   "$membername",
		                     -expires =>   "+1d");

		$passcookie = cookie(-name    =>   "adminpass",
		                     -value   =>   "$password_one",
		                     -expires =>   "+1d");

		print header(-cookie=>[$namecookie, $passcookie]); print start_html(-title=>"�������� ��������� Ikonboard", -bgcolor=>"#EEEEEE", -style=>{-code=>$stylesheet});

		print qq(
		<font size="5" face="Trebuchet MS" color="#000000">
		<h1>�������� ��������� Ikonboard</b></font></h1>
		<hr noshade size=1 color="#000000">
		<br>
		<font face="verdana" size="3" color="#000000">
		<b>����� ���������� � ��������� Ikonboard!</b>
		<br><br><font size=2>
		<b>��������� ���:</b><br>
		�������� ��������� Ikonboard ������ ������� ���������������� ������� (������� ������).
		<br>
		<hr noshade size=1 color="#000000">
		<br>
		);

		eval { ($0 =~ m,(.*)/[^/]+,)   && unshift (@INC, "$1"); ($0 =~ m,(.*)\\[^\\]+,) && unshift (@INC, "$1");
		require "data/boardinfo.cgi";
     };
     if ($@) {
     print header('text/html; charset=windows-1251'); print start_html(-title=>"������ Ikonboard!");
     print "���������� ����� ��������� �����: $@\n���� �� ��������� ��� NT �� ��� ����� ������������ ������ ������ ���� � ��������� ������� �������";
     print end_html; exit;
     }

		$currenttime = time;
		$blanks = "yes" if (!$membername);
		$blanks = "yes" if (!$password_one);
		$blanks = "yes" if (!$password_two);

		if ($blanks) { print qq(<br><br><font color="#FF0000" size="3"> ����������, ��������� ����� ���������, ����������� ������ �����, ����� ��������� ���� ���.); print end_html; exit; }
		if ($password_one ne $password_two)  { print qq(<br><br><font color="#FF0000" size="3">������, ������� �� �����, �� ���������������. ��������� ����� ��� ����������� ���� ������.); print end_html; exit; }

		$memberfilename = $membername;
		$memberfilename =~ y/ /_/;
		$membersdir = "$ikondir" . "members";

		$filetomake = "$ikondir" . "members/$memberfilename.cgi";

		open (ADMIN, ">$filetomake") or die "���������� ������� ���� $filetomake, ��������� ����!";
		print ADMIN "$membername|$password_one|Administrator|ad|0|$adminemail_in|no|private||||||$currenttime||";
		close (ADMIN);

		if (-e $filetomake) {
		print qq(
		<font face="verdana" size="2" color="#000000">
		<b>�����������, ���� Ikonboard �����������!.</b>
		<br><br>
		������ �� ������ <a href="admincenter.cgi?action=remove">������� � ����� ����������</a>, ��������� ������ � ������� ����������<br>. ���� �������� ��������� ������ ���� ����� �� �������� � ����� ����������. ��������� ��� �� ����� ������� �������� ����!<br>);
		}
		else {
        print qq(
		<font face="verdana" size="2" color="#FF0000">
		<b>������! � �� ���� ������� ���� ��������������!</b>
		<br><br>
		��������� ������� ����� ����� 'members': $membersdir );
		}

      $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        
        
       open(FILE, ">$filetomake");
       flock(FILE, 2);
       print FILE "\$lastregisteredmember = \"$membername\"\;\n";
       print FILE "\$totalmembers = \"1\"\;\n";
       print FILE "\$totalthreads = \"0\"\;\n";
       print FILE "\$totalposts = \"0\"\;\n";
       print FILE "\n1\;";
       close (FILE);

		print qq(
		<br><br>
		<hr noshade size=1 color="#000000">
		<font face="verdana" size="3" color="#0000FF">
		���������� �� ������������� Ikonboard!</font>
		<br><br>
		<font face="verdana" size="2" color="#000000">
		�� ��������, ��� ������������� ��������� ��������� Ikonboard ������� ���.<br>
		���� � ��� ���� ������ �������, �������� ��� <a href="http://www.ikonboard.com/cgi-bin/ikonboard.cgi"><b>����� ���������</b></a>
		<br><br>
		�������, <br>
		<i>������� Ikonboard</i>
		<br><br>
		);

		} # end final step   
    

            else {

				eval '$home = (getpwuid($<))[7];'; if (!-e "C:/") { $pwd = `pwd`; chop $pwd; } if (!eval 'use Cwd;') { eval '$cwd = cwd();'; } else { $cwd = ""; } $prog = $0;
				if ($prog =~ m|install\.(\w+)|) { $prog = "install.$1"; $cgi_extension = $1; } 
				$b4 = $`; $b4 =~ s/\/$//; $b4 =~ s/\\$//; $document_root = $ENV{'DOCUMENT_ROOT'}; $document_root =~ s/\/$//;
				$document_root =~ s/\\$//; $filename = $ENV{'SCRIPT_FILENAME'}; $filename =~ s/\/$prog//; $filename =~ s/\\$prog//;
				$path = $ENV{'PATH_TRANSLATED'}; $path =~ s/\/$//; $path =~ s/\\$//;
				&check($pwd); &check($b4); &check($home); &check($document_root); &check($filename); &check($path); &check($cwd);
				opendir(CURDIR, ".."); while ($q = readdir(CURDIR)) { push (@founddir, $q); }
				closedir(CURDIR); $true_path =~ s%\\%/%g; $true_path =~ s%//%/%g;
				if ($true_path =~ m|(.*)/(.+)|) { $base = $1; $cgi = $2; } else { $base = $true_path; $cgi = "cgi-bin"; }
				$poss_html_dir = "public_html htdocs"; $unsure_html_dir = "htdoc html www wwwdoc wwwdocs wwwroot httpd doc docs"; @poss = split(/\s/, $poss_html_dir);
				@founddir = grep(!/\./, @founddir); $checker = 0;
				foreach $test_dir (@poss) { if (grep(/^$test_dir$/, @founddir)) { $html_dir = "$base/$test_dir/ikonboard"; $checker = 1; last; } }
				if ($checker == 0) { @poss = split(/\s/, $unsure_html_dir); foreach $test_dir (@poss) {
				if (grep(/^$test_dir$/, @founddir)) { if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$html_dir = "$base/$test_dir/ikonboard"; if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$checker = 2; $test_dir_me = $test_dir; last; } else { $checker = 1; last; }
				} else { if (-e "$base/$test_dir/index.html" || -e "$base/$test_dir/index.htm" || -e "$base/$test_dir/index.php" || -e "$base/$test_dir/index.php3") {
				$html_dir = "$base/$test_dir/ikonboard"; $checker = 2; $test_dir_me = $test_dir; last; } else { $checker = 1; last; } } } } }
				if ($html_dir eq "") { $html_dir = "$base/ikonboard"; } $script_dir = "$true_path/ikonboard"; $test_ss = "";
				if ($ENV{'SCRIPT_URI'} ne "") { $test_ss = $ENV{'SCRIPT_URI'}; } elsif ($ENV{'SCRIPT_URL'} ne "") { $test_ss = $ENV{'SCRIPT_URL'};
				} elsif ($ENV{'REQUEST_URI'}) { $test_ss = $ENV{'REQUEST_URI'}; } elsif ($ENV{'SCRIPT_NAME'} ne "") { $test_ss = $ENV{'SCRIPT_NAME'}; }
				if ($test_ss ne "") { if ($test_ss =~ m|^http://([^/]+)|) { $test_ss = $'; } if ($test_ss =~ m|/$prog|) { $test_ss = $`; }
				if ($test_ss ne "") { $script_url = "http://$ENV{'HTTP_HOST'}$test_ss/ikonboard"; }
				} else { $script_url = "http://$ENV{'HTTP_HOST'}/$cgi/ikonboard"; }
				if ($script_url =~ m|^http://([^/]+)/~([^/]+)/|) { $uinfo = "~" . $2 . "/"; }
				$html_url = "http://$ENV{'HTTP_HOST'}/$uinfo" . "ikonboard"; $html_dir =~ s%/%\\%g if $html_dir =~ m|^(\w+):|; $script_dir =~ s%/%\\%g if $script_dir =~ m|^(\w+):|;
				$bdcgi = "$base/$cgi"; $html_dir =~ s%\\\\%\\%g; $script_dir =~ s%\\\\%\\%g; $bdcgi =~ s%\\\\%\\%g;
				if (-e "C:/" || $^O eq "MSWin32") { $OS_USED = 'NT'; }
				$adminemail_in = "incoming\@yourdomain.com"; $adminemail_out = "outgoing\@yourdomain.com";
				$timezone_choice = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\" selected>0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
				$time_is_now = localtime; $website_url = "http://$ENV{'HTTP_HOST'}";
				
                    print qq~
				    <form action="$thisprog" method="post">
				    <input type="hidden" name="action" value="step_two">
				    <font size="5" face="Trebuchet MS" color="#000000">
				    <h1>���o���� ��������� Ikonboard</b></font></h1>
				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>����� ���������� � ��������� Ikonboard!</b>
				    <br><br><font size=2>
				    <b>��� ����:</b> ��������� ��������� ����� �� ������ ���������� � �������� ������ ����� ��������� ���� �����.<br>
				    ����� �������� ���� ����� �������� ��������� �������� ��� �������� ������
				    � ���� ��� �����, ���� ���-�� �������� ��������.<br><br>
				    <b>����� ����������� ���� ��������� ���������, ��� ��� ����� ��������� ���������
				    � ����� ����������� ��������� CHMOD.</b><br><br>
				    ��� �������� ����� �������� ����� ���� �������� ����� ����� ����������. ��� ���������� ������ 
				    ������������, ���� ������ install.cgi ������ ���� ����� ����� ������� ���������� ���������. ���� ��� �����������, �� �������
				    ��� ��� ��������� ��� �� ������ � ��������� ��������� �������.</font><br>

				    <hr noshade size=1 color="#000000">

				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>� ����� ������������ ������� ����� �������� IkonBoard?</b><br><br>
				    <font face="verdana" size="2" color="#000000">
				    �������� ���-�� ����
				    <br>
				    <br>
				    <select name="OS_USED">
				    <option value="NT" >NT
				    <option value="Unix" selected>Unix
				    </select>

				    <br>
				    <br>
				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>��� ��������� ����� �� ����� �������?</b><br><br>
				    ��������� ��������� ��������� - ������ ���� ������ �������������. <font color="#FF0000"><br>������ ��������� ��� ��������� �, ���� ���-���� ���������,
				    �������� �� ���� �� ����� ���-�����.</font><br><br>
				    <font color="#FF0000">���� � ��� NT ������, ����������� ������� �������� �����! ('��������: c:\\path\\to\\ikonboard\\')
				    <br><font color="#000000"><b>��������� '/' (����) � ����� ���� �����</b>
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ����� ������������ *.cgi �������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��� ������ ���� 'path', a �� URL. �� <b>��</b> ����� ���������� � 'http://'.<br>
				    ��� ����� ������ ��������� ��� *.cgi �������, ������� ���������� � Ikonboard. ���������
				    ����� <b>������</b> ��� ���� ������� � ��������� � ���� ����������� �����.
				    <ul>
				    <li>data
				    <li>messages
				    <li>messages
				    <li>help
				    </ul><br>
				    <input type="text" size="70" name="ikondir" value="$script_dir/">
				    
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ��������� ��������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��� ������ ���� 'path', a �� URL. �� <b>��</b> ����� ���������� � 'http://'.<br>
				    ��� ����� ������ ��������� ��� ��������, ������� ���������� � Ikonboard. ���������
				    ����� <b>������</b> ��� ���� ������� � ��������� � ���� ����������� �����.
				    <br>
				    <b>�� ���������� '/images/' � ����� ����� ��������!</b>
				    
				    <ul>
				    <li>images
				    <li>emoticons
				    <li>avatars
				    </ul><br>
				    <input type="text" size="70" name="imagesdir" value="$html_dir/">
				    <br>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>����� URL ������ ���-�����?</b><br><br>
				    ��������� ��������� ��������� - ������ ���� ������ �������������. <font color="#FF0000"><br>������ ��������� ��� ��������� �, ���� ���-���� ���������,
				    �������� �� ���� �� ����� ���-�����.</font><br><br>
				    <b>�� ������� '/' (����) �� ����� ���� URL</b>
				    <br><br>

				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ����������� ��������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��� ������ ����'URL'. �� <b>������</b> ���������� � 'http://'.<br>
				    ��� ����� ������ ��������� ��� ��������, ������� ���������� � Ikonboard.
				    <br> 
				    <br><br>
				    <input type="text" size="70" name="imagesurl" value="$html_url">
				    <br><br>
				    
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ���������� ��� ����?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��� ������ ����'URL'. �� <b>������</b> ���������� � 'http://'.<br>
				    ��� ������� ���� �����, ������� �� ��������� � ��������, ����� ����� �� ���� ���-����.
				    <br><br>
				    <input type="text" size="70" name="homeurl" value="$website_url">

				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ����������� ���� Ikonboard?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��� ������ ����'URL'. �� <b>������</b>  ���������� � 'http://'.<br>
				    <b>�� ���������� 'ikonboard.cgi' � �����. ��� URL �����, � �� �����</b>.
				    <br><br>
				    <input type="text" size="70" name="boardurl" value="$script_url">

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>������� � ��������</b><br><br>
				    <font face="verdana" size="2" color="#000000">
				    ������� - ��� ��������, �������� ������������ ����� ���������� ���� � ����������.<br>
				    �������� ������������� � ������� ,��������  ':)'
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>������ �������� ��������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��������
				    <br><br>
				    <select name="avatars">
				    <option value="on" selected>���
				    <option value="off">����
				    </select>

				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>������ �������� ��������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ��������
				    <br><br>
				    <select name="emoticons">
				    <option value="on" selected>���
				    <option value="off">����
				    </select>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>E-mail</b><br><br>
				    ��������� ��������� ��������� - ������ ���� ������ �������������. <font color="#FF0000">������ ��������� ��� ��������� �, ���� ���-���� ���������,
				    �������� �� ���� �� ����� ���-�����.</font>
				    
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>������ �������� ������� e-mail?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ���� ��� �� ����� ��������� ������� e-mail, �������� '����'
				    � ���������� ��� ����� �������.
				    <br><br>
				    <select name="emailfunctions">
				    <option value="off">���� ������� E-MAIL
				    <option value="on" selected>��� ������� E-MAIL
				    </select>
				    <br><br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>����� �������� �������� ����� ��������������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    �������� �������� � ������� ����
				    <br><br>
				    <select name="emailtype">
				    <option value="smtp_mail" selected>SMTP
				    <option value="send_mail">Sendmail
				    <option value="blat_mail">Blat
				    </select>
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>SMTP ������ (���� �������)</b></font><br><br>
				    <input type=text size="60" name="SMTP_SERVER" value="localhost">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>���� � Sendmail (���� �������)</b></font><br><br>
				    <input type=text size="60" name="SEND_MAIL" value="/usr/lib/sendmail">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�������� e-mail</b></font><br><br>
				    <input type=text size="60" name="adminemail_in" value="$adminemail_in">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��������� e-mail</b></font><br><br>
				    <input type=text size="60" name="adminemail_out" value="$adminemail_out">
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�� ������ �������, ����� ������������ �������� ���� ������ ����� email, ��������� � Ikonboard?</b></font><br>
				    <br>
				    <br>
				    <select name="passwordverification">
				    <option value="no">���
				    <option value="yes" selected>��
				    </select>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>��������</b><br><br>
				    <font size=2>����� ��������� ������� ����� Ikonboard.</font>
				    <br>
				    
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�������� ����� Ikonboard</b></font><br>
				    <input type=text size="60" name="boardname" value="My Ikonboard">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�������� ����� Ikonboard</b></font><br>
				    <input type=text size="60" name="boarddescription" value="My Ikonboard for community building">
				    <br>

              <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ��������</b><br>�� ���� ��������� '&copy\;' - ������ ������� ��� ���.<br>
				    &copy\;</font><input type=text size="100" name="copyrightinfo" value="2000 My Website.com">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�������� �����</b></font><br>
				    <input type=text size="60" name="homename" value="ikondiscussion.com">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>������ �������� ������ �� �����?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    ������ �� ����� �������� ����� ������������� ������� ����������� ���������� �������, � ������� �������� ��� �� ������ ������� ���������. ��� �� ������ �� ��������������� ��� �������������, ������� �� ���������� �� ������ ����������.
				    <br>
				    <br>
				    <select name="floodcontrol">
				    <option value="off">��������� ������ �� �����
				    <option value="on" selected>�������� ������ �� �����
				    </select>
				    <br>
				    
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>���������� ������ ��� ������ �� ����� (���� ������� ������ �� �����)</b></font><br>
				    <input type=text size=10 name="floodcontrollimit" value="30"> &nbsp; ������
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>�������� ������� ����</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    �������� ������ ������� ������� $time_is_now. ���� ��� �������, �������������� ������� ��� ����������� ��������� ������� �������. 
				    <br>
				    <br>
				    $timezone_choice
				    <br>
				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>����� � ��� �����?</b></font><br><br>
				    <input type=text size="60" name="basetimes" value="GMT (UK)">
				    <br>

				    <br>
				    <font face="verdana" size="3" color="#0000FF">
				    <b>��� ����� ��������� ����� ��� ����������?</b></font><br>
				    <font face="verdana" size="2" color="#000000">
				    �� ��������� ���, ��� ��������������,
				    ������ ����� ���������� ��� ����.
				    <br>
				    <br>
				    <select name="announcements">
				    <option value="no">���
				    <option value="yes" selected>��
				    </select>
				    <br>

				    <hr noshade size=1 color="#000000">
				    <br>
				    <font face="verdana" size="3" color="#000000">
				    <b>������ �� ���������</b><br><br>
				    </font>
				    <br>
				    
				    <input type=submit value=submit>
				    </form>~;
				    }
    print end_html;
    exit(0);

sub check { local ($dr) = @_; return 0 if $dr eq ""; if (-e "$dr/$prog") { $true_path = $dr; return 1; } }

