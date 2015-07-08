from utils import detect_string, gen_hashcode
import time


KERNEL_PANIC = [
    r"(kernel BUG at[^\n]+)",
    r"(spinlock bad magic)",
    r"(Unable to handle kernel[^\n]+)",
    r"(modem subsystem failure reason:.*Could not turn on the UNIV_STMR ustmr_qtimer_off_counter)",
    r"(\w+ subsystem failure reason:[^\n]+)",
    r"(Kernel panic - not syncing: [^\n]*: Timed out waiting for error ready: modem)",
    r"(Kernel panic - [^\n]*)"
]

IGNORES = [
    r"Crash injected via Diag",
    r"SysRq : Trigger a crash"
]

def kernel_panic(logcat, headers):
    parts = logcat.split('\n\n')
    for content in parts[1:]:
        process = "kernel"
        for ignore in IGNORES:
            if detect_string(content, ignore):
                return None, None, None
        for pattern in KERNEL_PANIC:
            reason = detect_string(content, pattern)
            if reason:
                result = {'issue_owner': process, 'reason': reason}
                if "should check the ramdump" in reason:
                    result["random"] = time.time()
                md5 = gen_hashcode(result)
                return md5, result, None
    return None, None, None