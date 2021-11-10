async function drawLineChart() {

  // 1. Access data
  const dataset = [
  {
    "time_period_start": "2017-01-13T00:00:00.0000000Z",
    "time_period_end": "2017-01-14T00:00:00.0000000Z",
    "time_open": "2017-01-13T13:43:59.7020000Z",
    "time_close": "2017-01-13T23:28:37.9410000Z",
    "price_open": 9.72648,
    "price_high": 9.81939,
    "price_low": 9.5911,
    "price_close": 9.7978,
    "volume_traded": 8786.00326745,
    "trades_count": 202
  },
  {
    "time_period_start": "2017-01-14T00:00:00.0000000Z",
    "time_period_end": "2017-01-15T00:00:00.0000000Z",
    "time_open": "2017-01-14T00:09:06.5720000Z",
    "time_close": "2017-01-14T23:41:12.2570000Z",
    "price_open": 9.79999,
    "price_high": 9.89999,
    "price_low": 9.60162,
    "price_close": 9.60165,
    "volume_traded": 5109.81497106,
    "trades_count": 230
  },
  {
    "time_period_start": "2017-01-15T00:00:00.0000000Z",
    "time_period_end": "2017-01-16T00:00:00.0000000Z",
    "time_open": "2017-01-15T00:02:15.3900000Z",
    "time_close": "2017-01-15T23:45:36.8440000Z",
    "price_open": 9.6658,
    "price_high": 9.8823,
    "price_low": 9.66065,
    "price_close": 9.79079,
    "volume_traded": 4696.39046914,
    "trades_count": 258
  },
  {
    "time_period_start": "2017-01-16T00:00:00.0000000Z",
    "time_period_end": "2017-01-17T00:00:00.0000000Z",
    "time_open": "2017-01-16T00:20:56.1730000Z",
    "time_close": "2017-01-16T23:44:31.4060000Z",
    "price_open": 9.76,
    "price_high": 9.87164,
    "price_low": 9.59111,
    "price_close": 9.6081,
    "volume_traded": 6762.38572239,
    "trades_count": 270
  },
  {
    "time_period_start": "2017-01-17T00:00:00.0000000Z",
    "time_period_end": "2017-01-18T00:00:00.0000000Z",
    "time_open": "2017-01-17T00:00:04.4970000Z",
    "time_close": "2017-01-17T23:55:03.2370000Z",
    "price_open": 9.61999,
    "price_high": 10.688,
    "price_low": 9.61,
    "price_close": 10.23208,
    "volume_traded": 40357.19324679,
    "trades_count": 1592
  },
  {
    "time_period_start": "2017-01-18T00:00:00.0000000Z",
    "time_period_end": "2017-01-19T00:00:00.0000000Z",
    "time_open": "2017-01-18T00:06:05.5910000Z",
    "time_close": "2017-01-18T23:56:53.1630000Z",
    "price_open": 10.344,
    "price_high": 10.5,
    "price_low": 9.9,
    "price_close": 10.35,
    "volume_traded": 46755.34718016,
    "trades_count": 947
  },
  {
    "time_period_start": "2017-01-19T00:00:00.0000000Z",
    "time_period_end": "2017-01-20T00:00:00.0000000Z",
    "time_open": "2017-01-19T00:05:09.6730000Z",
    "time_close": "2017-01-19T23:59:22.6100000Z",
    "price_open": 10.34624,
    "price_high": 10.6,
    "price_low": 10.2,
    "price_close": 10.44988,
    "volume_traded": 23333.86986506,
    "trades_count": 471
  },
  {
    "time_period_start": "2017-01-20T00:00:00.0000000Z",
    "time_period_end": "2017-01-21T00:00:00.0000000Z",
    "time_open": "2017-01-20T00:03:14.3840000Z",
    "time_close": "2017-01-20T23:58:54.8500000Z",
    "price_open": 10.421,
    "price_high": 10.79221,
    "price_low": 10.25,
    "price_close": 10.62001,
    "volume_traded": 33399.10319808,
    "trades_count": 954
  },
  {
    "time_period_start": "2017-01-21T00:00:00.0000000Z",
    "time_period_end": "2017-01-22T00:00:00.0000000Z",
    "time_open": "2017-01-21T00:00:45.5740000Z",
    "time_close": "2017-01-21T23:45:11.4290000Z",
    "price_open": 10.65,
    "price_high": 11,
    "price_low": 10.57079,
    "price_close": 10.92204,
    "volume_traded": 20455.99327515,
    "trades_count": 582
  },
  {
    "time_period_start": "2017-01-22T00:00:00.0000000Z",
    "time_period_end": "2017-01-23T00:00:00.0000000Z",
    "time_open": "2017-01-22T00:45:32.6480000Z",
    "time_close": "2017-01-22T23:51:08.5870000Z",
    "price_open": 10.92154,
    "price_high": 11,
    "price_low": 10.5393,
    "price_close": 10.78807,
    "volume_traded": 16363.37576769,
    "trades_count": 504
  },
  {
    "time_period_start": "2017-01-23T00:00:00.0000000Z",
    "time_period_end": "2017-01-24T00:00:00.0000000Z",
    "time_open": "2017-01-23T00:02:47.8380000Z",
    "time_close": "2017-01-23T23:57:00.0910000Z",
    "price_open": 10.671,
    "price_high": 11.1971,
    "price_low": 10.6148,
    "price_close": 10.80851,
    "volume_traded": 24204.45692572,
    "trades_count": 398
  },
  {
    "time_period_start": "2017-01-24T00:00:00.0000000Z",
    "time_period_end": "2017-01-25T00:00:00.0000000Z",
    "time_open": "2017-01-24T00:00:07.1800000Z",
    "time_close": "2017-01-24T23:47:16.6670000Z",
    "price_open": 10.77942,
    "price_high": 10.77973,
    "price_low": 10.45063,
    "price_close": 10.5,
    "volume_traded": 16988.98674271,
    "trades_count": 504
  },
  {
    "time_period_start": "2017-01-25T00:00:00.0000000Z",
    "time_period_end": "2017-01-26T00:00:00.0000000Z",
    "time_open": "2017-01-25T00:02:47.5750000Z",
    "time_close": "2017-01-25T23:30:29.1530000Z",
    "price_open": 10.60643,
    "price_high": 10.667,
    "price_low": 10.41046,
    "price_close": 10.50829,
    "volume_traded": 12954.78536711,
    "trades_count": 296
  },
  {
    "time_period_start": "2017-01-26T00:00:00.0000000Z",
    "time_period_end": "2017-01-27T00:00:00.0000000Z",
    "time_open": "2017-01-26T00:01:10.2290000Z",
    "time_close": "2017-01-26T23:59:17.3940000Z",
    "price_open": 10.5138,
    "price_high": 10.691,
    "price_low": 10.44092,
    "price_close": 10.54,
    "volume_traded": 11224.58760326,
    "trades_count": 373
  },
  {
    "time_period_start": "2017-01-27T00:00:00.0000000Z",
    "time_period_end": "2017-01-28T00:00:00.0000000Z",
    "time_open": "2017-01-27T00:10:01.0290000Z",
    "time_close": "2017-01-27T23:51:43.8410000Z",
    "price_open": 10.51784,
    "price_high": 10.6532,
    "price_low": 10.38,
    "price_close": 10.58636,
    "volume_traded": 22961.77083513,
    "trades_count": 436
  },
  {
    "time_period_start": "2017-01-28T00:00:00.0000000Z",
    "time_period_end": "2017-01-29T00:00:00.0000000Z",
    "time_open": "2017-01-28T00:01:17.1940000Z",
    "time_close": "2017-01-28T23:12:30.7200000Z",
    "price_open": 10.5741,
    "price_high": 10.59996,
    "price_low": 10.4,
    "price_close": 10.5254,
    "volume_traded": 6203.94558779,
    "trades_count": 185
  },
  {
    "time_period_start": "2017-01-29T00:00:00.0000000Z",
    "time_period_end": "2017-01-30T00:00:00.0000000Z",
    "time_open": "2017-01-29T00:29:28.6200000Z",
    "time_close": "2017-01-29T23:11:22.9650000Z",
    "price_open": 10.52,
    "price_high": 10.54819,
    "price_low": 10.40754,
    "price_close": 10.43361,
    "volume_traded": 2087.5595765,
    "trades_count": 103
  },
  {
    "time_period_start": "2017-01-30T00:00:00.0000000Z",
    "time_period_end": "2017-01-31T00:00:00.0000000Z",
    "time_open": "2017-01-30T00:15:04.1690000Z",
    "time_close": "2017-01-30T23:59:10.1820000Z",
    "price_open": 10.46999,
    "price_high": 10.72889,
    "price_low": 10.42001,
    "price_close": 10.43574,
    "volume_traded": 15638.81042869,
    "trades_count": 401
  },
  {
    "time_period_start": "2017-01-31T00:00:00.0000000Z",
    "time_period_end": "2017-02-01T00:00:00.0000000Z",
    "time_open": "2017-01-31T00:20:02.7820000Z",
    "time_close": "2017-01-31T23:54:41.3340000Z",
    "price_open": 10.56,
    "price_high": 10.77419,
    "price_low": 10.49314,
    "price_close": 10.66911,
    "volume_traded": 12638.62021865,
    "trades_count": 364
  },
  {
    "time_period_start": "2017-02-01T00:00:00.0000000Z",
    "time_period_end": "2017-02-02T00:00:00.0000000Z",
    "time_open": "2017-02-01T00:10:21.6380000Z",
    "time_close": "2017-02-01T23:51:34.6290000Z",
    "price_open": 10.75997,
    "price_high": 10.7999,
    "price_low": 10.5279,
    "price_close": 10.59066,
    "volume_traded": 24214.02329515,
    "trades_count": 773
  },
  {
    "time_period_start": "2017-02-02T00:00:00.0000000Z",
    "time_period_end": "2017-02-03T00:00:00.0000000Z",
    "time_open": "2017-02-02T00:19:29.4210000Z",
    "time_close": "2017-02-02T23:51:41.1600000Z",
    "price_open": 10.6548,
    "price_high": 10.8596,
    "price_low": 10.56206,
    "price_close": 10.7705,
    "volume_traded": 12651.58883304,
    "trades_count": 351
  },
  {
    "time_period_start": "2017-02-03T00:00:00.0000000Z",
    "time_period_end": "2017-02-04T00:00:00.0000000Z",
    "time_open": "2017-02-03T00:02:59.8850000Z",
    "time_close": "2017-02-03T23:55:44.2470000Z",
    "price_open": 10.7705,
    "price_high": 10.98073,
    "price_low": 10.56124,
    "price_close": 10.98073,
    "volume_traded": 23956.94006842,
    "trades_count": 823
  },
  {
    "time_period_start": "2017-02-04T00:00:00.0000000Z",
    "time_period_end": "2017-02-05T00:00:00.0000000Z",
    "time_open": "2017-02-04T00:08:06.7660000Z",
    "time_close": "2017-02-04T23:51:40.6240000Z",
    "price_open": 10.99745,
    "price_high": 11.46718,
    "price_low": 10.99745,
    "price_close": 11.34979,
    "volume_traded": 32943.50910037,
    "trades_count": 789
  },
  {
    "time_period_start": "2017-02-05T00:00:00.0000000Z",
    "time_period_end": "2017-02-06T00:00:00.0000000Z",
    "time_open": "2017-02-05T01:18:15.8270000Z",
    "time_close": "2017-02-05T23:31:47.2560000Z",
    "price_open": 11.26771,
    "price_high": 11.37499,
    "price_low": 11.14,
    "price_close": 11.25399,
    "volume_traded": 8012.67324483,
    "trades_count": 228
  },
  {
    "time_period_start": "2017-02-06T00:00:00.0000000Z",
    "time_period_end": "2017-02-07T00:00:00.0000000Z",
    "time_open": "2017-02-06T00:18:03.8300000Z",
    "time_close": "2017-02-06T23:53:42.8900000Z",
    "price_open": 11.217,
    "price_high": 11.35719,
    "price_low": 11.17423,
    "price_close": 11.3,
    "volume_traded": 9875.1617995,
    "trades_count": 343
  },
  {
    "time_period_start": "2017-02-07T00:00:00.0000000Z",
    "time_period_end": "2017-02-08T00:00:00.0000000Z",
    "time_open": "2017-02-07T00:03:21.7280000Z",
    "time_close": "2017-02-07T23:56:35.2430000Z",
    "price_open": 11.27834,
    "price_high": 11.54298,
    "price_low": 11.278,
    "price_close": 11.43001,
    "volume_traded": 17183.65153978,
    "trades_count": 473
  },
  {
    "time_period_start": "2017-02-08T00:00:00.0000000Z",
    "time_period_end": "2017-02-09T00:00:00.0000000Z",
    "time_open": "2017-02-08T00:10:21.6690000Z",
    "time_close": "2017-02-08T23:52:17.4820000Z",
    "price_open": 11.45,
    "price_high": 11.54367,
    "price_low": 11.106,
    "price_close": 11.39262,
    "volume_traded": 20674.15223219,
    "trades_count": 600
  },
  {
    "time_period_start": "2017-02-09T00:00:00.0000000Z",
    "time_period_end": "2017-02-10T00:00:00.0000000Z",
    "time_open": "2017-02-09T00:21:37.7920000Z",
    "time_close": "2017-02-09T23:48:24.4710000Z",
    "price_open": 11.38878,
    "price_high": 11.5,
    "price_low": 10.4893,
    "price_close": 10.93949,
    "volume_traded": 57808.80626475,
    "trades_count": 1957
  },
  {
    "time_period_start": "2017-02-10T00:00:00.0000000Z",
    "time_period_end": "2017-02-11T00:00:00.0000000Z",
    "time_open": "2017-02-10T00:01:43.9680000Z",
    "time_close": "2017-02-10T23:48:06.1220000Z",
    "price_open": 10.93886,
    "price_high": 11.4078,
    "price_low": 10.804,
    "price_close": 11.3495,
    "volume_traded": 22975.73589447,
    "trades_count": 724
  },
  {
    "time_period_start": "2017-02-11T00:00:00.0000000Z",
    "time_period_end": "2017-02-12T00:00:00.0000000Z",
    "time_open": "2017-02-11T00:01:22.3720000Z",
    "time_close": "2017-02-11T23:40:36.8480000Z",
    "price_open": 11.34999,
    "price_high": 11.4455,
    "price_low": 11.25,
    "price_close": 11.41999,
    "volume_traded": 26778.61805705,
    "trades_count": 816
  },
  {
    "time_period_start": "2017-02-12T00:00:00.0000000Z",
    "time_period_end": "2017-02-13T00:00:00.0000000Z",
    "time_open": "2017-02-12T00:04:00.4090000Z",
    "time_close": "2017-02-12T23:54:03.2320000Z",
    "price_open": 11.38949,
    "price_high": 11.3993,
    "price_low": 11.24821,
    "price_close": 11.3649,
    "volume_traded": 9755.23566171,
    "trades_count": 314
  },
  {
    "time_period_start": "2017-02-13T00:00:00.0000000Z",
    "time_period_end": "2017-02-14T00:00:00.0000000Z",
    "time_open": "2017-02-13T00:02:17.9970000Z",
    "time_close": "2017-02-13T23:55:36.8550000Z",
    "price_open": 11.38991,
    "price_high": 11.39,
    "price_low": 11.15677,
    "price_close": 11.31341,
    "volume_traded": 10844.38164881,
    "trades_count": 416
  },
  {
    "time_period_start": "2017-02-14T00:00:00.0000000Z",
    "time_period_end": "2017-02-15T00:00:00.0000000Z",
    "time_open": "2017-02-14T02:47:04.9550000Z",
    "time_close": "2017-02-14T23:58:14.6640000Z",
    "price_open": 11.4,
    "price_high": 13.58998,
    "price_low": 11.38173,
    "price_close": 13.1847,
    "volume_traded": 126099.59112629,
    "trades_count": 2819
  },
  {
    "time_period_start": "2017-02-15T00:00:00.0000000Z",
    "time_period_end": "2017-02-16T00:00:00.0000000Z",
    "time_open": "2017-02-15T00:03:35.3270000Z",
    "time_close": "2017-02-15T23:57:48.5770000Z",
    "price_open": 13.03951,
    "price_high": 13.171,
    "price_low": 12.60343,
    "price_close": 12.99848,
    "volume_traded": 46304.35838607,
    "trades_count": 932
  },
  {
    "time_period_start": "2017-02-16T00:00:00.0000000Z",
    "time_period_end": "2017-02-17T00:00:00.0000000Z",
    "time_open": "2017-02-16T00:00:28.4030000Z",
    "time_close": "2017-02-16T23:56:10.6990000Z",
    "price_open": 12.98001,
    "price_high": 13.02928,
    "price_low": 12.49,
    "price_close": 12.9,
    "volume_traded": 57710.50404732,
    "trades_count": 1439
  },
  {
    "time_period_start": "2017-02-17T00:00:00.0000000Z",
    "time_period_end": "2017-02-18T00:00:00.0000000Z",
    "time_open": "2017-02-17T00:01:47.2130000Z",
    "time_close": "2017-02-17T23:53:46.1560000Z",
    "price_open": 12.9,
    "price_high": 12.91,
    "price_low": 12.66963,
    "price_close": 12.70031,
    "volume_traded": 16059.45330669,
    "trades_count": 407
  },
  {
    "time_period_start": "2017-02-18T00:00:00.0000000Z",
    "time_period_end": "2017-02-19T00:00:00.0000000Z",
    "time_open": "2017-02-18T00:17:32.5630000Z",
    "time_close": "2017-02-18T22:56:14.3870000Z",
    "price_open": 12.70152,
    "price_high": 12.90998,
    "price_low": 12.70002,
    "price_close": 12.8,
    "volume_traded": 9690.32668867,
    "trades_count": 176
  },
  {
    "time_period_start": "2017-02-19T00:00:00.0000000Z",
    "time_period_end": "2017-02-20T00:00:00.0000000Z",
    "time_open": "2017-02-19T01:21:30.0170000Z",
    "time_close": "2017-02-19T23:31:50.0390000Z",
    "price_open": 12.83904,
    "price_high": 12.89,
    "price_low": 12.69,
    "price_close": 12.80999,
    "volume_traded": 5570.16881451,
    "trades_count": 175
  },
  {
    "time_period_start": "2017-02-20T00:00:00.0000000Z",
    "time_period_end": "2017-02-21T00:00:00.0000000Z",
    "time_open": "2017-02-20T00:00:24.5630000Z",
    "time_close": "2017-02-20T23:59:52.2360000Z",
    "price_open": 12.7813,
    "price_high": 12.91,
    "price_low": 12.43,
    "price_close": 12.47,
    "volume_traded": 22892.21899404,
    "trades_count": 570
  },
  {
    "time_period_start": "2017-02-21T00:00:00.0000000Z",
    "time_period_end": "2017-02-22T00:00:00.0000000Z",
    "time_open": "2017-02-21T00:00:06.9520000Z",
    "time_close": "2017-02-21T23:59:46.1640000Z",
    "price_open": 12.43,
    "price_high": 12.84022,
    "price_low": 12.2288,
    "price_close": 12.78238,
    "volume_traded": 25369.65033514,
    "trades_count": 651
  },
  {
    "time_period_start": "2017-02-22T00:00:00.0000000Z",
    "time_period_end": "2017-02-23T00:00:00.0000000Z",
    "time_open": "2017-02-22T00:01:51.2960000Z",
    "time_close": "2017-02-22T23:35:24.1010000Z",
    "price_open": 12.7305,
    "price_high": 12.79998,
    "price_low": 12.62623,
    "price_close": 12.69549,
    "volume_traded": 18555.41431039,
    "trades_count": 381
  },
  {
    "time_period_start": "2017-02-23T00:00:00.0000000Z",
    "time_period_end": "2017-02-24T00:00:00.0000000Z",
    "time_open": "2017-02-23T00:32:14.0420000Z",
    "time_close": "2017-02-23T23:57:14.7150000Z",
    "price_open": 12.6272,
    "price_high": 13.3,
    "price_low": 12.6272,
    "price_close": 13.09401,
    "volume_traded": 30950.59584045,
    "trades_count": 782
  },
  {
    "time_period_start": "2017-02-24T00:00:00.0000000Z",
    "time_period_end": "2017-02-25T00:00:00.0000000Z",
    "time_open": "2017-02-24T00:00:58.2380000Z",
    "time_close": "2017-02-24T23:25:32.7960000Z",
    "price_open": 13.19998,
    "price_high": 13.3,
    "price_low": 12.56,
    "price_close": 13.03808,
    "volume_traded": 45688.94452967,
    "trades_count": 1233
  },
  {
    "time_period_start": "2017-02-25T00:00:00.0000000Z",
    "time_period_end": "2017-02-26T00:00:00.0000000Z",
    "time_open": "2017-02-25T00:16:47.8120000Z",
    "time_close": "2017-02-25T23:27:45.4690000Z",
    "price_open": 13.1,
    "price_high": 13.75,
    "price_low": 13.00003,
    "price_close": 13.5717,
    "volume_traded": 32644.97900621,
    "trades_count": 928
  },
  {
    "time_period_start": "2017-02-26T00:00:00.0000000Z",
    "time_period_end": "2017-02-27T00:00:00.0000000Z",
    "time_open": "2017-02-26T00:15:27.0030000Z",
    "time_close": "2017-02-26T23:50:00.8820000Z",
    "price_open": 13.41022,
    "price_high": 14.46989,
    "price_low": 13.33035,
    "price_close": 14.44,
    "volume_traded": 81710.08554678,
    "trades_count": 1775
  },
  {
    "time_period_start": "2017-02-27T00:00:00.0000000Z",
    "time_period_end": "2017-02-28T00:00:00.0000000Z",
    "time_open": "2017-02-27T00:06:19.7020000Z",
    "time_close": "2017-02-27T23:58:02.0530000Z",
    "price_open": 14.478,
    "price_high": 15.73988,
    "price_low": 14.25,
    "price_close": 15.37071,
    "volume_traded": 58114.61757537,
    "trades_count": 1572
  },
  {
    "time_period_start": "2017-02-28T00:00:00.0000000Z",
    "time_period_end": "2017-03-01T00:00:00.0000000Z",
    "time_open": "2017-02-28T00:02:24.5060000Z",
    "time_close": "2017-02-28T23:59:33.8140000Z",
    "price_open": 15.37532,
    "price_high": 16.06055,
    "price_low": 15.01231,
    "price_close": 15.63,
    "volume_traded": 142838.38647542,
    "trades_count": 3272
  },
  {
    "time_period_start": "2017-03-01T00:00:00.0000000Z",
    "time_period_end": "2017-03-02T00:00:00.0000000Z",
    "time_open": "2017-03-01T00:00:34.7690000Z",
    "time_close": "2017-03-01T23:58:25.1910000Z",
    "price_open": 15.62999,
    "price_high": 17.3,
    "price_low": 15.45281,
    "price_close": 17.3,
    "volume_traded": 81782.54477116,
    "trades_count": 1928
  },
  {
    "time_period_start": "2017-03-02T00:00:00.0000000Z",
    "time_period_end": "2017-03-03T00:00:00.0000000Z",
    "time_open": "2017-03-02T00:00:12.6860000Z",
    "time_close": "2017-03-02T23:59:30.0520000Z",
    "price_open": 17.3,
    "price_high": 19.23,
    "price_low": 16.05,
    "price_close": 18.9871,
    "volume_traded": 187479.33988966,
    "trades_count": 4515
  },
  {
    "time_period_start": "2017-03-03T00:00:00.0000000Z",
    "time_period_end": "2017-03-04T00:00:00.0000000Z",
    "time_open": "2017-03-03T00:00:45.0620000Z",
    "time_close": "2017-03-03T23:57:36.7740000Z",
    "price_open": 18.98,
    "price_high": 20.49,
    "price_low": 16.75,
    "price_close": 19.11001,
    "volume_traded": 182909.91875414,
    "trades_count": 5085
  },
  {
    "time_period_start": "2017-03-04T00:00:00.0000000Z",
    "time_period_end": "2017-03-05T00:00:00.0000000Z",
    "time_open": "2017-03-04T00:00:20.2420000Z",
    "time_close": "2017-03-04T23:57:20.1650000Z",
    "price_open": 19.36785,
    "price_high": 19.9,
    "price_low": 18.35273,
    "price_close": 18.58567,
    "volume_traded": 45644.34495339,
    "trades_count": 1435
  },
  {
    "time_period_start": "2017-03-05T00:00:00.0000000Z",
    "time_period_end": "2017-03-06T00:00:00.0000000Z",
    "time_open": "2017-03-05T00:01:32.8450000Z",
    "time_close": "2017-03-05T23:53:14.2610000Z",
    "price_open": 18.45003,
    "price_high": 19.47037,
    "price_low": 17.9,
    "price_close": 19.03258,
    "volume_traded": 41409.43196832,
    "trades_count": 1198
  },
  {
    "time_period_start": "2017-03-06T00:00:00.0000000Z",
    "time_period_end": "2017-03-07T00:00:00.0000000Z",
    "time_open": "2017-03-06T00:01:54.5340000Z",
    "time_close": "2017-03-06T23:55:46.1520000Z",
    "price_open": 19.05001,
    "price_high": 20,
    "price_low": 18.8,
    "price_close": 19.5,
    "volume_traded": 47203.76571351,
    "trades_count": 1352
  },
  {
    "time_period_start": "2017-03-07T00:00:00.0000000Z",
    "time_period_end": "2017-03-08T00:00:00.0000000Z",
    "time_open": "2017-03-07T00:03:45.7060000Z",
    "time_close": "2017-03-07T23:50:44.6740000Z",
    "price_open": 19.38962,
    "price_high": 19.78522,
    "price_low": 18.35001,
    "price_close": 18.82279,
    "volume_traded": 69146.41333177,
    "trades_count": 1945
  },
  {
    "time_period_start": "2017-03-08T00:00:00.0000000Z",
    "time_period_end": "2017-03-09T00:00:00.0000000Z",
    "time_open": "2017-03-08T00:06:24.7570000Z",
    "time_close": "2017-03-08T23:59:52.9970000Z",
    "price_open": 18.63486,
    "price_high": 18.72,
    "price_low": 16.4,
    "price_close": 16.4,
    "volume_traded": 80599.00994275,
    "trades_count": 2281
  },
  {
    "time_period_start": "2017-03-09T00:00:00.0000000Z",
    "time_period_end": "2017-03-10T00:00:00.0000000Z",
    "time_open": "2017-03-09T00:01:09.9170000Z",
    "time_close": "2017-03-09T23:56:55.3390000Z",
    "price_open": 16.40001,
    "price_high": 17.99,
    "price_low": 15.56,
    "price_close": 17.59999,
    "volume_traded": 108947.57800991,
    "trades_count": 3001
  },
  {
    "time_period_start": "2017-03-10T00:00:00.0000000Z",
    "time_period_end": "2017-03-11T00:00:00.0000000Z",
    "time_open": "2017-03-10T00:06:47.8510000Z",
    "time_close": "2017-03-10T23:59:37.7020000Z",
    "price_open": 17.59998,
    "price_high": 19.75847,
    "price_low": 15.9,
    "price_close": 19.25,
    "volume_traded": 238609.77789732,
    "trades_count": 6449
  },
  {
    "time_period_start": "2017-03-11T00:00:00.0000000Z",
    "time_period_end": "2017-03-12T00:00:00.0000000Z",
    "time_open": "2017-03-11T00:01:52.1910000Z",
    "time_close": "2017-03-11T23:55:40.6860000Z",
    "price_open": 19.24993,
    "price_high": 21.39997,
    "price_low": 18.65007,
    "price_close": 21.28997,
    "volume_traded": 116906.88257044,
    "trades_count": 3152
  },
  {
    "time_period_start": "2017-03-12T00:00:00.0000000Z",
    "time_period_end": "2017-03-13T00:00:00.0000000Z",
    "time_open": "2017-03-12T00:03:30.5120000Z",
    "time_close": "2017-03-12T23:59:23.5310000Z",
    "price_open": 21.24999,
    "price_high": 23.398,
    "price_low": 20.9999,
    "price_close": 23.30013,
    "volume_traded": 122275.02755307,
    "trades_count": 3822
  },
  {
    "time_period_start": "2017-03-13T00:00:00.0000000Z",
    "time_period_end": "2017-03-14T00:00:00.0000000Z",
    "time_open": "2017-03-13T00:00:50.7340000Z",
    "time_close": "2017-03-13T23:59:43.4690000Z",
    "price_open": 23.31,
    "price_high": 30.67504,
    "price_low": 23.16007,
    "price_close": 28.19957,
    "volume_traded": 324933.29029897,
    "trades_count": 10242
  },
  {
    "time_period_start": "2017-03-14T00:00:00.0000000Z",
    "time_period_end": "2017-03-15T00:00:00.0000000Z",
    "time_open": "2017-03-14T00:01:09.4680000Z",
    "time_close": "2017-03-14T23:53:52.1760000Z",
    "price_open": 28.19997,
    "price_high": 29.83,
    "price_low": 26.401,
    "price_close": 28.37047,
    "volume_traded": 97239.79085247,
    "trades_count": 3223
  },
  {
    "time_period_start": "2017-03-15T00:00:00.0000000Z",
    "time_period_end": "2017-03-16T00:00:00.0000000Z",
    "time_open": "2017-03-15T00:05:54.4710000Z",
    "time_close": "2017-03-15T23:59:49.8500000Z",
    "price_open": 28.37245,
    "price_high": 34.80999,
    "price_low": 28.00021,
    "price_close": 34.75,
    "volume_traded": 154328.4177962,
    "trades_count": 4464
  },
  {
    "time_period_start": "2017-03-16T00:00:00.0000000Z",
    "time_period_end": "2017-03-17T00:00:00.0000000Z",
    "time_open": "2017-03-16T00:00:14.2080000Z",
    "time_close": "2017-03-16T23:59:59.9560000Z",
    "price_open": 34.74999,
    "price_high": 45,
    "price_low": 34.7467,
    "price_close": 44.89,
    "volume_traded": 143813.55664527,
    "trades_count": 6394
  },
  {
    "time_period_start": "2017-03-17T00:00:00.0000000Z",
    "time_period_end": "2017-03-18T00:00:00.0000000Z",
    "time_open": "2017-03-17T00:00:41.9340000Z",
    "time_close": "2017-03-17T23:59:00.3090000Z",
    "price_open": 44.86976,
    "price_high": 51.9,
    "price_low": 35,
    "price_close": 42.52908,
    "volume_traded": 238515.57558494,
    "trades_count": 11913
  },
  {
    "time_period_start": "2017-03-18T00:00:00.0000000Z",
    "time_period_end": "2017-03-19T00:00:00.0000000Z",
    "time_open": "2017-03-18T00:00:04.2210000Z",
    "time_close": "2017-03-18T23:59:36.9060000Z",
    "price_open": 42.52957,
    "price_high": 43.99995,
    "price_low": 30.30025,
    "price_close": 33.202,
    "volume_traded": 196897.61339027,
    "trades_count": 7247
  },
  {
    "time_period_start": "2017-03-19T00:00:00.0000000Z",
    "time_period_end": "2017-03-20T00:00:00.0000000Z",
    "time_open": "2017-03-19T00:00:39.5480000Z",
    "time_close": "2017-03-19T23:58:58.4530000Z",
    "price_open": 33.49975,
    "price_high": 44.96982,
    "price_low": 32.51373,
    "price_close": 42.36041,
    "volume_traded": 140627.23769583,
    "trades_count": 6541
  },
  {
    "time_period_start": "2017-03-20T00:00:00.0000000Z",
    "time_period_end": "2017-03-21T00:00:00.0000000Z",
    "time_open": "2017-03-20T00:00:44.4620000Z",
    "time_close": "2017-03-20T23:59:21.7810000Z",
    "price_open": 42.36109,
    "price_high": 44.74,
    "price_low": 40.21,
    "price_close": 41.89,
    "volume_traded": 69514.67522854,
    "trades_count": 3694
  },
  {
    "time_period_start": "2017-03-21T00:00:00.0000000Z",
    "time_period_end": "2017-03-22T00:00:00.0000000Z",
    "time_open": "2017-03-21T00:00:23.2250000Z",
    "time_close": "2017-03-21T23:59:27.5880000Z",
    "price_open": 41.89003,
    "price_high": 43.19823,
    "price_low": 41.02229,
    "price_close": 42.48308,
    "volume_traded": 46201.86383967,
    "trades_count": 2682
  },
  {
    "time_period_start": "2017-03-22T00:00:00.0000000Z",
    "time_period_end": "2017-03-23T00:00:00.0000000Z",
    "time_open": "2017-03-22T00:02:49.4880000Z",
    "time_close": "2017-03-22T23:58:19.6330000Z",
    "price_open": 42.00558,
    "price_high": 42.69665,
    "price_low": 37.6,
    "price_close": 41.24972,
    "volume_traded": 51480.6233759,
    "trades_count": 2669
  },
  {
    "time_period_start": "2017-03-23T00:00:00.0000000Z",
    "time_period_end": "2017-03-24T00:00:00.0000000Z",
    "time_open": "2017-03-23T00:07:41.9010000Z",
    "time_close": "2017-03-23T23:58:06.3050000Z",
    "price_open": 41.2,
    "price_high": 44,
    "price_low": 40,
    "price_close": 42.70261,
    "volume_traded": 50806.63188085,
    "trades_count": 2803
  },
  {
    "time_period_start": "2017-03-24T00:00:00.0000000Z",
    "time_period_end": "2017-03-25T00:00:00.0000000Z",
    "time_open": "2017-03-24T00:00:39.8380000Z",
    "time_close": "2017-03-24T23:59:58.8810000Z",
    "price_open": 42.71065,
    "price_high": 52.89999,
    "price_low": 42.52,
    "price_close": 51.99,
    "volume_traded": 134845.32851723,
    "trades_count": 6470
  },
  {
    "time_period_start": "2017-03-25T00:00:00.0000000Z",
    "time_period_end": "2017-03-26T00:00:00.0000000Z",
    "time_open": "2017-03-25T00:00:10.6590000Z",
    "time_close": "2017-03-25T23:59:31.5340000Z",
    "price_open": 51.80011,
    "price_high": 52.56613,
    "price_low": 46.7,
    "price_close": 50,
    "volume_traded": 80167.72809612,
    "trades_count": 5128
  },
  {
    "time_period_start": "2017-03-26T00:00:00.0000000Z",
    "time_period_end": "2017-03-27T00:00:00.0000000Z",
    "time_open": "2017-03-26T00:00:03.4420000Z",
    "time_close": "2017-03-26T23:59:12.9040000Z",
    "price_open": 49.99934,
    "price_high": 50.93841,
    "price_low": 47.90001,
    "price_close": 49.99999,
    "volume_traded": 38621.72887868,
    "trades_count": 2689
  },
  {
    "time_period_start": "2017-03-27T00:00:00.0000000Z",
    "time_period_end": "2017-03-28T00:00:00.0000000Z",
    "time_open": "2017-03-27T00:00:20.8890000Z",
    "time_close": "2017-03-27T23:49:18.0180000Z",
    "price_open": 49.99218,
    "price_high": 51.202,
    "price_low": 48.05,
    "price_close": 48.71658,
    "volume_traded": 43230.14218806,
    "trades_count": 3410
  },
  {
    "time_period_start": "2017-03-28T00:00:00.0000000Z",
    "time_period_end": "2017-03-29T00:00:00.0000000Z",
    "time_open": "2017-03-28T00:00:24.1750000Z",
    "time_close": "2017-03-28T23:59:44.9920000Z",
    "price_open": 48.83888,
    "price_high": 50.49999,
    "price_low": 48.11111,
    "price_close": 50.23688,
    "volume_traded": 54142.31248521,
    "trades_count": 4630
  },
  {
    "time_period_start": "2017-03-29T00:00:00.0000000Z",
    "time_period_end": "2017-03-30T00:00:00.0000000Z",
    "time_open": "2017-03-29T00:00:09.3710000Z",
    "time_close": "2017-03-29T23:53:59.3820000Z",
    "price_open": 50.23639,
    "price_high": 53.97999,
    "price_low": 50,
    "price_close": 53.01498,
    "volume_traded": 83583.67268808,
    "trades_count": 4915
  },
  {
    "time_period_start": "2017-03-30T00:00:00.0000000Z",
    "time_period_end": "2017-03-31T00:00:00.0000000Z",
    "time_open": "2017-03-30T00:00:15.6250000Z",
    "time_close": "2017-03-30T23:58:11.3190000Z",
    "price_open": 52.99999,
    "price_high": 54.97531,
    "price_low": 51.10001,
    "price_close": 51.89999,
    "volume_traded": 41012.29652505,
    "trades_count": 2798
  },
  {
    "time_period_start": "2017-03-31T00:00:00.0000000Z",
    "time_period_end": "2017-04-01T00:00:00.0000000Z",
    "time_open": "2017-03-31T00:02:26.9840000Z",
    "time_close": "2017-03-31T23:51:12.8710000Z",
    "price_open": 51.75,
    "price_high": 51.75,
    "price_low": 46.60152,
    "price_close": 49.6975,
    "volume_traded": 73653.10985132,
    "trades_count": 4621
  },
  {
    "time_period_start": "2017-04-01T00:00:00.0000000Z",
    "time_period_end": "2017-04-02T00:00:00.0000000Z",
    "time_open": "2017-04-01T00:01:33.5210000Z",
    "time_close": "2017-04-01T23:59:23.6170000Z",
    "price_open": 49.69,
    "price_high": 51.8,
    "price_low": 48.56928,
    "price_close": 50.6398,
    "volume_traded": 27374.25456918,
    "trades_count": 2115
  },
  {
    "time_period_start": "2017-04-02T00:00:00.0000000Z",
    "time_period_end": "2017-04-03T00:00:00.0000000Z",
    "time_open": "2017-04-02T00:10:25.6970000Z",
    "time_close": "2017-04-02T23:59:37.8040000Z",
    "price_open": 50.62269,
    "price_high": 51.2713,
    "price_low": 47.38002,
    "price_close": 48.4995,
    "volume_traded": 45444.42632427,
    "trades_count": 3518
  },
  {
    "time_period_start": "2017-04-03T00:00:00.0000000Z",
    "time_period_end": "2017-04-04T00:00:00.0000000Z",
    "time_open": "2017-04-03T00:00:13.3950000Z",
    "time_close": "2017-04-03T23:59:31.8030000Z",
    "price_open": 48.32507,
    "price_high": 48.4977,
    "price_low": 42.60848,
    "price_close": 44.11541,
    "volume_traded": 85803.79366675,
    "trades_count": 5583
  },
  {
    "time_period_start": "2017-04-04T00:00:00.0000000Z",
    "time_period_end": "2017-04-05T00:00:00.0000000Z",
    "time_open": "2017-04-04T00:02:38.5780000Z",
    "time_close": "2017-04-04T23:53:37.6070000Z",
    "price_open": 43.79901,
    "price_high": 45.78866,
    "price_low": 41.18512,
    "price_close": 44.74849,
    "volume_traded": 63906.24324325,
    "trades_count": 3580
  },
  {
    "time_period_start": "2017-04-05T00:00:00.0000000Z",
    "time_period_end": "2017-04-06T00:00:00.0000000Z",
    "time_open": "2017-04-05T00:08:43.8510000Z",
    "time_close": "2017-04-05T23:58:17.7790000Z",
    "price_open": 44.40987,
    "price_high": 47.18919,
    "price_low": 44.025,
    "price_close": 45.283,
    "volume_traded": 44562.15273348,
    "trades_count": 3057
  },
  {
    "time_period_start": "2017-04-06T00:00:00.0000000Z",
    "time_period_end": "2017-04-07T00:00:00.0000000Z",
    "time_open": "2017-04-06T00:02:29.7800000Z",
    "time_close": "2017-04-06T23:59:49.5460000Z",
    "price_open": 45.25004,
    "price_high": 45.94929,
    "price_low": 41.01,
    "price_close": 43.4099,
    "volume_traded": 50251.890832,
    "trades_count": 3661
  },
  {
    "time_period_start": "2017-04-07T00:00:00.0000000Z",
    "time_period_end": "2017-04-08T00:00:00.0000000Z",
    "time_open": "2017-04-07T00:01:40.5420000Z",
    "time_close": "2017-04-07T23:59:08.0570000Z",
    "price_open": 43.251,
    "price_high": 44.8092,
    "price_low": 41.75001,
    "price_close": 42.24,
    "volume_traded": 16323.42494375,
    "trades_count": 2417
  },
  {
    "time_period_start": "2017-04-08T00:00:00.0000000Z",
    "time_period_end": "2017-04-09T00:00:00.0000000Z",
    "time_open": "2017-04-08T00:00:22.6250000Z",
    "time_close": "2017-04-08T23:59:20.7460000Z",
    "price_open": 42.23455,
    "price_high": 45.79999,
    "price_low": 42.07233,
    "price_close": 44.33113,
    "volume_traded": 25870.6319975,
    "trades_count": 2986
  },
  {
    "time_period_start": "2017-04-09T00:00:00.0000000Z",
    "time_period_end": "2017-04-10T00:00:00.0000000Z",
    "time_open": "2017-04-09T00:00:03.9930000Z",
    "time_close": "2017-04-09T23:58:24.4840000Z",
    "price_open": 44.30502,
    "price_high": 44.99963,
    "price_low": 43.21,
    "price_close": 43.93521,
    "volume_traded": 19770.86852323,
    "trades_count": 2037
  },
  {
    "time_period_start": "2017-04-10T00:00:00.0000000Z",
    "time_period_end": "2017-04-11T00:00:00.0000000Z",
    "time_open": "2017-04-10T00:12:35.4940000Z",
    "time_close": "2017-04-10T23:53:24.5550000Z",
    "price_open": 43.80009,
    "price_high": 44.79949,
    "price_low": 42.1,
    "price_close": 43.7,
    "volume_traded": 22565.12288807,
    "trades_count": 1860
  },
  {
    "time_period_start": "2017-04-11T00:00:00.0000000Z",
    "time_period_end": "2017-04-12T00:00:00.0000000Z",
    "time_open": "2017-04-11T00:07:25.8820000Z",
    "time_close": "2017-04-11T23:58:29.8000000Z",
    "price_open": 43.7,
    "price_high": 44.601,
    "price_low": 43.52,
    "price_close": 43.95189,
    "volume_traded": 11969.4111852,
    "trades_count": 1431
  },
  {
    "time_period_start": "2017-04-12T00:00:00.0000000Z",
    "time_period_end": "2017-04-13T00:00:00.0000000Z",
    "time_open": "2017-04-12T00:07:49.9540000Z",
    "time_close": "2017-04-12T23:56:49.3100000Z",
    "price_open": 43.9366,
    "price_high": 47.94816,
    "price_low": 42.72,
    "price_close": 46.5019,
    "volume_traded": 42325.88802936,
    "trades_count": 3430
  },
  {
    "time_period_start": "2017-04-13T00:00:00.0000000Z",
    "time_period_end": "2017-04-14T00:00:00.0000000Z",
    "time_open": "2017-04-13T00:04:16.4820000Z",
    "time_close": "2017-04-13T23:56:27.9540000Z",
    "price_open": 46.20117,
    "price_high": 50.961,
    "price_low": 46.19999,
    "price_close": 50.0923,
    "volume_traded": 59237.11818746,
    "trades_count": 4898
  },
  {
    "time_period_start": "2017-04-14T00:00:00.0000000Z",
    "time_period_end": "2017-04-15T00:00:00.0000000Z",
    "time_open": "2017-04-14T00:00:06.7990000Z",
    "time_close": "2017-04-14T23:59:38.7340000Z",
    "price_open": 49.86001,
    "price_high": 50.0156,
    "price_low": 46.56381,
    "price_close": 47.33002,
    "volume_traded": 33513.98337716,
    "trades_count": 3516
  },
  {
    "time_period_start": "2017-04-15T00:00:00.0000000Z",
    "time_period_end": "2017-04-16T00:00:00.0000000Z",
    "time_open": "2017-04-15T00:02:18.0120000Z",
    "time_close": "2017-04-15T23:38:32.7400000Z",
    "price_open": 47.83868,
    "price_high": 49.6,
    "price_low": 47.05008,
    "price_close": 49.3289,
    "volume_traded": 12579.58729536,
    "trades_count": 1664
  },
  {
    "time_period_start": "2017-04-16T00:00:00.0000000Z",
    "time_period_end": "2017-04-17T00:00:00.0000000Z",
    "time_open": "2017-04-16T00:04:30.9680000Z",
    "time_close": "2017-04-16T23:58:13.0150000Z",
    "price_open": 48.75013,
    "price_high": 49,
    "price_low": 47.5,
    "price_close": 48.55612,
    "volume_traded": 5799.58826998,
    "trades_count": 1007
  },
  {
    "time_period_start": "2017-04-17T00:00:00.0000000Z",
    "time_period_end": "2017-04-18T00:00:00.0000000Z",
    "time_open": "2017-04-17T00:05:21.4830000Z",
    "time_close": "2017-04-17T23:55:57.9290000Z",
    "price_open": 48.11168,
    "price_high": 48.98004,
    "price_low": 47.5,
    "price_close": 47.8,
    "volume_traded": 18665.18498044,
    "trades_count": 1798
  },
  {
    "time_period_start": "2017-04-18T00:00:00.0000000Z",
    "time_period_end": "2017-04-19T00:00:00.0000000Z",
    "time_open": "2017-04-18T00:03:17.9970000Z",
    "time_close": "2017-04-18T23:59:53.9530000Z",
    "price_open": 47.80147,
    "price_high": 50.7348,
    "price_low": 47.61293,
    "price_close": 49.9084,
    "volume_traded": 37941.18578778,
    "trades_count": 3837
  },
  {
    "time_period_start": "2017-04-19T00:00:00.0000000Z",
    "time_period_end": "2017-04-20T00:00:00.0000000Z",
    "time_open": "2017-04-19T00:12:15.3490000Z",
    "time_close": "2017-04-19T23:59:59.2040000Z",
    "price_open": 49.90853,
    "price_high": 50.44879,
    "price_low": 45.27637,
    "price_close": 48,
    "volume_traded": 28549.3461158,
    "trades_count": 3048
  },
  {
    "time_period_start": "2017-04-20T00:00:00.0000000Z",
    "time_period_end": "2017-04-21T00:00:00.0000000Z",
    "time_open": "2017-04-20T00:00:10.7550000Z",
    "time_close": "2017-04-20T23:54:17.8510000Z",
    "price_open": 48.00001,
    "price_high": 49.55,
    "price_low": 47.25802,
    "price_close": 49.31,
    "volume_traded": 27363.7386562,
    "trades_count": 2125
  },
  {
    "time_period_start": "2017-04-21T00:00:00.0000000Z",
    "time_period_end": "2017-04-22T00:00:00.0000000Z",
    "time_open": "2017-04-21T00:02:12.8240000Z",
    "time_close": "2017-04-21T23:56:17.3520000Z",
    "price_open": 49.3399,
    "price_high": 49.44998,
    "price_low": 48,
    "price_close": 48.20003,
    "volume_traded": 21812.29153758,
    "trades_count": 1435
  },
  {
    "time_period_start": "2017-04-22T00:00:00.0000000Z",
    "time_period_end": "2017-04-23T00:00:00.0000000Z",
    "time_open": "2017-04-22T00:00:55.6950000Z",
    "time_close": "2017-04-22T23:54:25.4960000Z",
    "price_open": 48.20006,
    "price_high": 48.7465,
    "price_low": 47.5,
    "price_close": 48.20001,
    "volume_traded": 11331.35064473,
    "trades_count": 963
  }
];
  console.log(dataset);

  const yAccessor = d => d.price_high
  const dateParser = d3.timeParse("%Y-%m-%dT%H:%M:%S")
  const xAccessor = d => dateParser(d.time_period_end.split('.')[0])

  // 2. Create chart dimensions

  let dimensions = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight *0.75,
    margin: {
      top: 15,
      right: 15,
      bottom: 40,
      left: 60,
    },
  }
  dimensions.boundedWidth = dimensions.width
    - dimensions.margin.left
    - dimensions.margin.right
  dimensions.boundedHeight = dimensions.height
    - dimensions.margin.top
    - dimensions.margin.bottom

  // 3. Draw canvas

  const wrapper = d3.select("#wrapper")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

  const bounds = wrapper.append("g")
      .style("transform", `translate(${
        dimensions.margin.left
      }px, ${
        dimensions.margin.top
      }px)`)

  // 4. Create scales

  const yScale = d3.scaleLinear()
    .domain(d3.extent(dataset, yAccessor))
    .range([dimensions.boundedHeight, 0])

  // const freezingTemperaturePlacement = yScale(32)
  // const freezingTemperatures = bounds.append("rect")
  //     .attr("x", 0)
  //     .attr("width", dimensions.boundedWidth)
  //     .attr("y", freezingTemperaturePlacement)
  //     .attr("height", dimensions.boundedHeight
  //       - freezingTemperaturePlacement)
  //     .attr("fill", "#e0f3f3")

  const xScale = d3.scaleTime()
    .domain(d3.extent(dataset, xAccessor))
    .range([0, dimensions.boundedWidth])

  // 5. Draw data

  const lineGenerator = d3.line()
    .x(d => xScale(xAccessor(d)))
    .y(d => yScale(yAccessor(d)))

  const line = bounds.append("path")
      .attr("d", lineGenerator(dataset))
      .attr("fill", "none")
      .attr("stroke", "#af9358")
      .attr("stroke-width", 2)

  // 6. Draw peripherals

  const yAxisGenerator = d3.axisLeft()
    .scale(yScale)

  const yAxis = bounds.append("g")
    .call(yAxisGenerator)

  const xAxisGenerator = d3.axisBottom()
    .scale(xScale)

  const xAxis = bounds.append("g")
    .call(xAxisGenerator)
      .style("transform", `translateY(${
        dimensions.boundedHeight
      }px)`)
}

drawLineChart()
