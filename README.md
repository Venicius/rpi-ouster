# rpi-ouster
Setting Static IP on an Interface:
Edit the interfaces file with this command (vim or your favorite text editor)
sudo vim /etc/network/interfaces

Substitute eth1 for the name of your interface that you would like to bind to the 10.5.5.1 IP address.
eth0 on my machine is used to connect to the internet, which is why I left it using DHCP. If you want to do the same, then just replace eth0 with the name of your internet interface.

# interfaces(5) file used by ifup(8) and ifdown(8)

# Loopback interface for local connections
auto lo
iface lo inet loopback

#Interface for getting to the Internet
auto eth0
iface eth0 inet dhcp

# Interface to bind for use with the OS1 lidar
auto eth1
iface eth1 inet static
address 10.5.5.1
netmask 255.255.255.0

"For these settings to take effect you need to restart your networking services."

sudo /etc/init.d/networking restart

# ouster-lidar-rpi

### Configuração do Raspberry pi 4 com Mate Desktop

#### Instalar dnsmasq
``` sudo apt install dnsmasq dnsmasq-utils ```

#### Configuração de rede rasp + Ouster Lidar

Com o cabo desconectado executar os seguintes comandos no terminal:

``` ip addr flush dev eth0 ```

``` ip addr show dev eth0```

``` sudo ip addr add 10.5.5.1/24 dev eth0 ```

Conectar o cabo de rede e executar:

``` sudo ip link set eth0 up```

``` ip addr show dev eth0```

``` sudo dnsmasq -C /dev/null -kd -F 10.5.5.50,10.5.5.100 -i eth0 --bind-dynamic```

Aguardar entre 10 e 15 segundos, será mostrado o IP do Ouster com o Hostname ao final, por exemplo:

```dnsmasq-dhcp: DHPACK(eth0) <NUMERO IP> xx:xx:xx:xx:xx:xx os-9900123456```

O número ip fornecido no resultado acima, deve ser utilizado no scritp para captura do stream de dados do ouster.

Para testar se a conexão está ok, basta enviar um ping:
``` ping <NUMERO IP>```

