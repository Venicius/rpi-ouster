# ouster-lidar-rpi

### Configuração do Raspberry pi 4

#### Ip do Raspberry pi

É necessário que o raspberry pi esteja na mesma rede que o sensor ouster, que usa a faixa de ip 10.5.5.0;
No raspberry inserir o ip padrao <strong>10.5.5.1</strong>, caso seja outro ip diferente, deve-se mudar no codigo do programa.

#### Instalar dnsmasq

`sudo apt install dnsmasq dnsmasq-utils`

#### Configuração de rede rasp + Ouster Lidar

Com o cabo desconectado executar os seguintes comandos no terminal:

`ip addr flush dev eth0`

` ip addr show dev eth0`

`sudo ip addr add 10.5.5.1/24 dev eth0`

Conectar o cabo de rede e executar:

` sudo ip link set eth0 up`

` ip addr show dev eth0`

` sudo dnsmasq -C /dev/null -kd -F 10.5.5.86,10.5.5.86 -i eth0 --bind-dynamic`

Aguardar entre 10 e 15 segundos, será mostrado o IP do Ouster com o Hostname ao final, por exemplo:

`dnsmasq-dhcp: DHPACK(eth0) <NUMERO IP> xx:xx:xx:xx:xx:xx os-9900123456`

O número ip fornecido no resultado acima, deve ser utilizado no scritp para captura do stream de dados do ouster.

Para testar se a conexão está ok, basta enviar um ping:
` ping <NUMERO IP>`

Deve ser retornado o ip <strong>10.5.5.86 </strong>, caso seja um ip diferente, alterar no código do programa python.
