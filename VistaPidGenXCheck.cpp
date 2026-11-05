// VistaPidGenXCheck.cpp
// Read-only PidGenX diagnostic for Windows Vista SP2 x64.
// Does not install a key, activate Windows, or make network requests.
// Compatible with Visual C++ 2008.

#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <iostream>
#include <string>
#include <iomanip>

typedef HRESULT (WINAPI *PFN_PIDGENX)(
    WCHAR*, WCHAR*, WCHAR*, int, void*, void*, void*);

// Public PidGenX output buffers contain ASCII/UTF-16LE text with zero padding.
// Stop at a UTF-16 NUL pair, but skip embedded zero bytes so ASCII and UTF-16LE
// representations are both decoded correctly.
static std::string ReadPidGenXString(const unsigned char* data,
                                     size_t total, size_t offset)
{
    std::string out;
    if (offset >= total) return out;
    size_t i = offset;
    while (i < total) {
        if (i + 1 < total && data[i] == 0 && data[i + 1] == 0)
            break;
        if (data[i] != 0)
            out.push_back(static_cast<char>(data[i]));
        ++i;
    }
    return out;
}

static void PrintField(const char* label, const unsigned char* data,
                       size_t total, size_t offset)
{
    std::cout << label << ReadPidGenXString(data, total, offset) << "\n";
}

int wmain()
{
    const wchar_t* dllPath = L"C:\\Windows\\System32\\pidgenx.dll";
    const wchar_t* configPath =
        L"C:\\Windows\\System32\\licensing\\pkeyconfig\\pkeyconfig.xrm-ms";

    if (GetFileAttributesW(dllPath) == INVALID_FILE_ATTRIBUTES) {
        std::wcerr << L"ERROR: Vista x64 pidgenx.dll not found.\n";
        return 2;
    }
    if (GetFileAttributesW(configPath) == INVALID_FILE_ATTRIBUTES) {
        std::wcerr << L"ERROR: Vista PKEY configuration not found.\n";
        return 3;
    }

    std::wcout << L"Vista PidGenX read-only checker (x64)\n"
               << L"Enter a key locally. It is not saved or transmitted.\n\n"
               << L"Product key: ";

    std::wstring key;
    std::getline(std::wcin, key);
    if (key.empty() || key.size() >= 64) {
        std::wcerr << L"Invalid input length.\n";
        return 4;
    }

    HMODULE module = LoadLibraryW(dllPath);
    if (!module) {
        std::wcerr << L"LoadLibrary failed, Win32 error " << GetLastError() << L".\n";
        SecureZeroMemory(&key[0], key.size() * sizeof(wchar_t));
        return 5;
    }

    PFN_PIDGENX fn = reinterpret_cast<PFN_PIDGENX>(
        GetProcAddress(module, "PidGenX"));
    if (!fn) {
        std::wcerr << L"PidGenX export not found.\n";
        FreeLibrary(module);
        SecureZeroMemory(&key[0], key.size() * sizeof(wchar_t));
        return 6;
    }

    unsigned char pid[0x32] = { 0 };
    unsigned char dpid[0xA4] = { 0 };
    unsigned char dpid4[0x4F8] = { 0 };
    pid[0] = 0x32;
    dpid[0] = 0xA4;
    dpid4[0] = 0xF8;
    dpid4[1] = 0x04;
    WCHAR mspid[] = L"XXXXX";

    HRESULT hr = fn(&key[0], const_cast<WCHAR*>(configPath),
                    mspid, 0, pid, dpid, dpid4);

    SecureZeroMemory(&key[0], key.size() * sizeof(wchar_t));
    FreeLibrary(module);

    std::cout << "\nPidGenX HRESULT: 0x" << std::hex << std::uppercase
              << static_cast<unsigned long>(hr) << std::dec << "\n";

    if (hr == 0) {
        std::cout << "Local PidGenX result: accepted by this installed DLL/config pair.\n";
        PrintField("Product ID: ", pid, sizeof(pid), 0x0000);
        PrintField("Advanced PID: ", dpid4, sizeof(dpid4), 0x0008);
        PrintField("Activation ID: ", dpid4, sizeof(dpid4), 0x0088);
        PrintField("Edition type: ", dpid4, sizeof(dpid4), 0x0118);
        PrintField("Edition ID: ", dpid4, sizeof(dpid4), 0x0378);
        PrintField("Key type: ", dpid4, sizeof(dpid4), 0x03F8);
        PrintField("EULA: ", dpid4, sizeof(dpid4), 0x0478);
        std::cout << "\nThis is an offline key/configuration check only. "
                     "It does not prove licence ownership, genuine licensing, "
                     "or activation status.\n";
    } else if (static_cast<unsigned long>(hr) == 0x80070057UL) {
        std::cout << "PidGenX reported invalid arguments. Check local DLL/config paths.\n";
    } else {
        std::cout << "PidGenX did not accept this key/config input. "
                     "This is not an activation result.\n";
    }

    std::cout << "\nPress Enter to exit...";
    std::string wait;
    std::getline(std::cin, wait);
    return hr == 0 ? 0 : 1;
}
