import { NextResponse } from "next/server";
import axios from "axios"; // Corrected import

// To handle a GET request to /api
export async function GET(
    request,
    { params }
) {
    try {
        const { code } = params;
        const response = await axios.get("http://10.5.0.6:8000");
        const data = response.data;
        return NextResponse.json({ message: "Hello guys!", data: data, code: code }, { status: 200 });
    } catch (error) {
        console.error("Error fetching data:", error);
        return NextResponse.json({ message: "Error fetching data" }, { status: 500 });
    }
}

// To handle a POST request to /api
export async function POST(request, { params }) {
    const { code } = params;
    return NextResponse.json({ message: "Hello guys!", code: code }, { status: 200 });
}
