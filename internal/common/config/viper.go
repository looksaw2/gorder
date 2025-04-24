package config

import "github.com/spf13/viper"

func NewViperConfig() error {

	//设置
	viper.SetConfigName("global")
	viper.SetConfigType("yaml")
	//从order目录下读取配置文件
	viper.AddConfigPath("../common/config")
	viper.AutomaticEnv() //读取环境变量
	return viper.ReadInConfig()
}
