<html>
<body>
<style>
.absolute {
  position: absolute;
  top: 100px;
  left: 320px;
  right: 0;
  width: 600px;
  height: 120px;
}
</style>
<div class="absolute">
<span style="font-family: Arial-MT; font-size: 18px; line-height: 21px">
<span style="font-weight: bold">
${customer['xxxx']}
<br>${customer['surname']}
</span>
<br>${customer['address']}
<br>Tarifa ${customer['tariff']}
<br>
% if customer['lang'] == 'ca_ES':
 Pot&egrave;ncia
% else:
 Potencia
% endif
${customer['power']} kW
</span>
</div>
</body>
</html>
