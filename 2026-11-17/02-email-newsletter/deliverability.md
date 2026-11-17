# Deliverability checklist for a newsletter

Work through this before the first send to a list. Replace `example.com` with the domain the email comes from. Whoever runs the domain sets the DNS records. Thresholds below are common guidance, so check your mailing provider's own rules too.

1. **SPF.** One TXT record on the sending domain, such as `v=spf1 include:<your provider's SPF host> ~all`. A domain should have only one SPF record.
2. **DKIM.** Your provider gives you a selector and a public key. Publish them as a TXT record at `<selector>._domainkey.example.com`. Confirm the provider shows the key as verified.
3. **DMARC.** A TXT record at `_dmarc.example.com` such as `v=DMARC1; p=none; rua=mailto:<reports mailbox>; adkim=r; aspf=r`. Start at `p=none` and read the weekly reports. Move to `p=quarantine`, then `p=reject`, only after clean reports for several weeks.
4. **One-click unsubscribe.** Bulk senders to Gmail and Yahoo need a List-Unsubscribe header and `List-Unsubscribe-Post: List-Unsubscribe=One-Click`. Most providers add these when the email has an unsubscribe link. Confirm yours does.
5. **Visible unsubscribe and postal address.** Both belong in the footer. The check.mjs script looks for the link.
6. **Warm up.** Start with the people who opened or replied most recently, a few hundred at a time. Grow the volume over about two weeks. Hold the volume flat if bounces or spam complaints rise.
7. **Seed test.** Send a copy to a few test inboxes (Gmail, Outlook and Yahoo are a useful spread). Check that it lands in the inbox, not spam or promotions.
8. **Clean the list.** Remove addresses that bounced. Stop mailing people who have not opened anything in about six months.
