export async function POST(
    req, res
) {
    const j = await req.json();
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('x');
    const a = req.url.split("/");
    const body = req.body;

    return Response.json({ data: "hello", r: a[4], s: a[5], v: a[6], x: id, val: j.n }, { headers: { "Content-Type": "application/json" }, status: 200 });
}