
import axios from "axios";
import {config as settings} from "../../../../config/config"

export const config = {
  api: {
    bodyParser: false,
  },
};

async function handler(req: any, res: any) {
  if (req.method == "POST") {
    const { data } = await axios.post(settings.API_URL_FILES_UPLOAD, req, {
      responseType: "stream",
      headers: {
        "Content-Type": req.headers["content-type"]
      },
    });
    data.pipe(res);
  } else {
    return res.status(405).json({ message: "Method Not Allowed" });
  }
}

export default handler;