from regshield.agents.rule_collector import collect_rule

def main():
    rules = [
        ("RBI", "Digital Lending Guidelines", "https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12135"),
        ("RBI", "Digital Lending FAQ", "https://rbi.org.in/Scripts/FAQView.aspx?Id=137"),
        ("RBI", "Data Localization Circular", "https://rbi.org.in/Scripts/NotificationUser.aspx?Id=11244"),
        ("RBI", "Outsourcing of IT Services", "https://rbi.org.in/Scripts/NotificationUser.aspx?Id=12197"),
        ("RBI", "Cyber Security Framework", "https://rbi.org.in/Scripts/NotificationUser.aspx?Id=11605"),
    ]

    success = 0

    for src, title, url in rules:
        print("Collecting:", title)
        ok = collect_rule(src, title, url)
        if ok:
            success += 1

    print("SUCCESS COUNT:", success)

if __name__ == "__main__":
    main()
