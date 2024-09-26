```php
<?php

class class000 {
    private $payl0ad = 0;
    protected $what;

    public function __destruct()
    {
        $this->check();
    }

    public function check()
    {
        if($this->payl0ad === 0)
        {
            die('FAILED TO ATTACK');
        }
        $a = $this->what;
        $a();
    }
}

class class001 {
    public $payl0ad;
    public $a;
    public function __invoke()
    {
        $this->a->payload = $this->payl0ad;
    }
}

class class002 {
    private $sec;
    public function __set($a, $b)
    {
        $this->$b($this->sec);
    }

    public function dangerous($whaattt)
    {
        $whaattt->evvval($this->sec);
    }

}

class class003 {
    public $mystr;
    public function evvval($str)
    {
        eval($str);
    }

    public function __tostring()
    {
        return $this->mystr;
    }
}

if(isset($_GET['data']))
{
    $a = unserialize($_GET['data']);
}
else {
    highlight_file(__FILE__);
}
```

首先对于__set函数的陌生，

__set()方法的作用是为私有成员属性设置值，它含有两个参数，第一个参数是要赋值的属性名，第二个参数是要給属性赋的值，没有返回值，这个方法同样不用手动调用，实在设置私有属性值得时候自动调用的



```php
<?php
class Person{
	private $name;private $sex;private $age;
	function __get($property_name){
		echo '在直接获取私有属性值得时候,自动调用了这个__get()方法<br/>';
		if(isset($this->$property_name)){
			return ($this->$property_name);
		}else{
			return NULL;
		}	
	}
	function __set($property_name,$value){
		echo '在直接设置私有属性值得时候，自动调用了这个__set()方法为私有属性赋值<br/>';
		$this->$property_name=$value;
	}
}
$p1=new Person();
$p1->name='张三';$p1->sex='男';$p1->age=20;
echo '姓名：'.$p1->name.'<br/>';
echo '性别：'.$p1->sex.'<br/>';
echo '年龄：'.$p1->age.'<br/>';
```

