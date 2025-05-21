const axios = require("axios");
const express = require("express");
const cors = require("cors");
const path = require("path");
const app = express();

// Middleware
app.use(cors()); // Cho phép tất cả origin
app.use(express.json()); // Parse JSON body
app.use(express.static(path.join(__dirname, 'public'))); // Phục vụ file tĩnh từ thư mục public

// Route GET cho đường dẫn gốc
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html')); // Phục vụ index.html
  console.log("Serving index.html for GET /");
});

// Route POST cho thanh toán MoMo
app.post("/payment", async (req, res) => {
  const { amount, orderInfo } = req.body; // Nhận amount và orderInfo từ client
  console.log("Request body:", req.body); // Debug body nhận được

  // Kiểm tra dữ liệu đầu vào
  if (!amount || !orderInfo) {
    return res.status(400).json({
      statusCode: 400,
      message: "Thiếu amount hoặc orderInfo",
    });
  }

  const accessKey = 'F8BBA842ECF85';
  const secretKey = 'K951B6PE1waDMi640xX08PD3vg6EkVlz';
  const partnerCode = 'MOMO';
  const redirectUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b';
  const ipnUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b';
  const requestType = "payWithMethod";
  const orderId = partnerCode + new Date().getTime();
  const requestId = orderId;
  const extraData = '';
  const orderGroupId = '';
  const autoCapture = true;
  const lang = 'vi';

  // Tạo rawSignature
  const rawSignature = `accessKey=${accessKey}&amount=${amount}&extraData=${extraData}&ipnUrl=${ipnUrl}&orderId=${orderId}&orderInfo=${orderInfo}&partnerCode=${partnerCode}&redirectUrl=${redirectUrl}&requestId=${requestId}&requestType=${requestType}`;
  
  console.log("--------------------RAW SIGNATURE----------------");
  console.log(rawSignature);

  // Tạo chữ ký HMAC SHA256
  const crypto = require('crypto');
  const signature = crypto.createHmac('sha256', secretKey)
    .update(rawSignature)
    .digest('hex');
  console.log("--------------------SIGNATURE----------------");
  console.log(signature);

  // JSON object gửi đến MoMo
  const requestBody = JSON.stringify({
    partnerCode: partnerCode,
    partnerName: "Test",
    storeId: "MomoTestStore",
    requestId: requestId,
    amount: amount,
    orderId: orderId,
    orderInfo: orderInfo,
    redirectUrl: redirectUrl,
    ipnUrl: ipnUrl,
    lang: lang,
    requestType: requestType,
    autoCapture: autoCapture,
    extraData: extraData,
    orderGroupId: orderGroupId,
    signature: signature,
  });

  // Gửi yêu cầu đến MoMo API
  const options = {
    method: "POST",
    url: "https://test-payment.momo.vn/v2/gateway/api/create",
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(requestBody),
    },
    data: requestBody,
  };

  try {
    const result = await axios(options);
    console.log("MoMo response:", result.data); // Debug phản hồi từ MoMo
    return res.status(200).json(result.data);
  } catch (error) {
    console.error("MoMo error:", error.response ? error.response.data : error.message);
    return res.status(500).json({
      statusCode: 500,
      message: "Lỗi khi gọi MoMo API",
      error: error.response ? error.response.data : error.message,
    });
  }
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
