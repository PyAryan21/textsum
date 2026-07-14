def run(sentences: list[tuple[str, float]], num_lines: int) -> list[tuple[str, float]]:
    n = len(sentences)
    if n == 0:
        return []

    selected = [False] * n
    num_to_select = num_lines if num_lines < n else n

    for i, (sent, score) in enumerate(sentences):
        selected[i] = i < num_to_select

    while True:
        print("\n" + "=" * 60)
        for i, (sent, score) in enumerate(sentences):
            marker = "+" if selected[i] else " "
            bar = "#" * round(score * 20)
            pct = f"{score * 100:.0f}%"
            print(f"  [{marker}] {i+1:>3}. {bar} {pct:>4}  {sent[:80]}{'...' if len(sent)>80 else ''}")
        print("=" * 60)
        msg = f"\nCommands: <enter> to confirm | <num> to toggle | <range> like 1-5 | 'q' to quit\n> "
        try:
            cmd = input(msg).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if cmd == "":
            break
        if cmd == "q":
            return []

        parts = cmd.replace(",", " ").split()
        for part in parts:
            if "-" in part:
                try:
                    a, b = part.split("-")
                    for idx in range(int(a) - 1, int(b)):
                        if 0 <= idx < n:
                            selected[idx] = not selected[idx]
                except ValueError:
                    pass
            else:
                try:
                    idx = int(part) - 1
                    if 0 <= idx < n:
                        selected[idx] = not selected[idx]
                except ValueError:
                    pass

    return [sentences[i] for i in range(n) if selected[i]]
