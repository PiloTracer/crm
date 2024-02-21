import { NextResponse } from "next/server";
import axios from "axios"; // Corrected import

// To handle a GET request to /api
export async function GET(request) {
    try {
        const response = await axios.get("http://10.5.0.6:8000"); // Corrected declaration
        const data = response.data; // Use this data if needed
        return NextResponse.json({ message: "Hello guys!", data: data }, { status: 200 });
    } catch (error) {
        console.error("Error fetching data:", error);
        return NextResponse.json({ message: "Error fetching data" }, { status: 500 });
    }
}

// To handle a POST request to /api
export async function POST(request) {
    // Do whatever you want
    return NextResponse.json({ message: "Hello guys!" }, { status: 200 });
}
