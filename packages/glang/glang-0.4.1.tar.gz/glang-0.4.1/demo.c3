@require_once "std/format.c3"

function main : (argc: int, argv: u8[&][&]) -> int = {
    printf(sv("Hello, world! argc: %"), argc);
    return 0;
}
