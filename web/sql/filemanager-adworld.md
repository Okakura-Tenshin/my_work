### filemanager-adworld

首先目录爆破，可以看到有源代码泄露

upload.php

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午8:45
 */

require_once "common.inc.php";

if ($_FILES) {
	$file = $_FILES["upfile"];
	if ($file["error"] == UPLOAD_ERR_OK) {
		$name = basename($file["name"]);
		$path_parts = pathinfo($name);

		if (!in_array($path_parts["extension"], array("gif", "jpg", "png", "zip", "txt"))) {
			exit("error extension");
		}
		$path_parts["extension"] = "." . $path_parts["extension"];

		$name = $path_parts["filename"] . $path_parts["extension"];

		// $path_parts["filename"] = $db->quote($path_parts["filename"]);
		// Fix
		$path_parts['filename'] = addslashes($path_parts['filename']);

		$sql = "select * from `file` where `filename`='{$path_parts['filename']}' and `extension`='{$path_parts['extension']}'";

		$fetch = $db->query($sql);

		if ($fetch->num_rows > 0) {
			exit("file is exists");
		}

		if (move_uploaded_file($file["tmp_name"], UPLOAD_DIR . $name)) {

			$sql = "insert into `file` ( `filename`, `view`, `extension`) values( '{$path_parts['filename']}', 0, '{$path_parts['extension']}')";
			$re = $db->query($sql);
			if (!$re) {
				print_r($db->error);
				exit;
			}
			$url = "/" . UPLOAD_DIR . $name;
			echo "Your file is upload, url:
                <a href=\"{$url}\" target='_blank'>{$url}</a><br/>
                <a href=\"/\">go back</a>";
		} else {
			exit("upload error");
		}

	} else {
		print_r(error_get_last());
		exit;
	}
}
```

delete.php

```php
require_once "common.inc.php";

if(isset($req['filename'])) {
    $result = $db->query("select * from `file` where `filename`='{$req['filename']}'");
    if ($result->num_rows>0){
        $result = $result->fetch_assoc();
    }

    $filename = UPLOAD_DIR . $result["filename"] . $result["extension"];
    if ($result && file_exists($filename)) {
        $db->query('delete from `file` where `fid`=' . $result["fid"]);
        unlink($filename);
        redirect("/");
    }
}
```

rename.php

```php
if (isset($req['oldname']) && isset($req['newname'])) {
	$result = $db->query("select * from `file` where `filename`='{$req['oldname']}'");
	if ($result->num_rows > 0) {
		$result = $result->fetch_assoc();
	} else {
		exit("old file doesn't exists!");
	}

	if ($result) {

		$req['newname'] = basename($req['newname']);
		$re = $db->query("update `file` set `filename`='{$req['newname']}', `oldname`='{$result['filename']}' where `fid`={$result['fid']}");
		if (!$re) {
			print_r($db->error);
			exit;
		}
		$oldname = UPLOAD_DIR . $result["filename"] . $result["extension"];
		$newname = UPLOAD_DIR . $req["newname"] . $result["extension"];
		if (file_exists($oldname)) {
			rename($oldname, $newname);
		}
		$url = "/" . $newname;
		echo "Your file is rename, url:
                <a href=\"{$url}\" target='_blank'>{$url}</a><br/>
                <a href=\"/\">go back</a>";
	}
}
?>
```

数据库配置

```sql
SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS `xdctf`;
CREATE DATABASE xdctf;
USE xdctf;

DROP TABLE IF EXISTS `file`;
CREATE TABLE `file` (
  `fid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `filename` varchar(256) NOT NULL,
  `oldname` varchar(256) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `extension` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

```

通过代码审计可以发现，在upload中与sql数据库的设置，addslashes函数与utf-8编码基本杜绝了宽字节的注入

