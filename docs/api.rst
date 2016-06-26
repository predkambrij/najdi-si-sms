Python API
++++++++++

Example::

  from najdisi_sms import SMSSender

  sms = SMSSender('username', 'password')
  sms.send(
      '031123456',
      'Pikica, rad te mam. (sent from cronjob)'
  )
