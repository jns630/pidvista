// VistaPidGenXCheck.cpp
// Read-only PidGenX diagnostic for Windows Vista SP2 x64.
// Calls the locally installed Vista pidgenx.dll and pkeyconfig.xrm-ms.
// It does NOT install a key, activate Windows, or make network requests.
// Compatible with the Visual C++ 2008 language level.

#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0600
#include <windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

// PidGenX export signature used by public PIDX wrappers. On x64 Windows the
// platform ABI is unified; WINAPI is retained for source compatibility.
typedef HRESULT (WINAPI *PFN_PIDGENX)(
    WCHAR* productKey,
    WCHAR* pkeyConfigPath,
    WCHAR* mspid,
    int usage,
    void* productId,
    void* digitalProductId,
    void* digitalProductId4);

static std::string ReadAsciiField(const unsigned char* p, size_t capacity)
{
    size_t n = 0;
    while (n < capacity && p[n] != 0) ++n;
    return std::string(reinterpret_cast<const char*>(p), n);
}

static void PrintField(const char* label, const unsigned char* blob,
                       size_t offset, size_t capacity)
{
    std::cout << label << ReadAsciiField(blob + offset, capacity) << "\n";
}

int wmain()
{
    const wchar_t* dllPath = L"C:\\Windows\\System32\\pidgenx.dll";
    const wchar_t* configPath =
        L"C:\\Windows\\System32\\licensing\\pkeyconfig\\pkeyconfig.xrm-ms";

    DWORD attrs = GetFileAttributesW(dllPath);
    if (attrs == INVALID_FILE_ATTRIBUTES) {
        std::wcerr << L"ERROR: Vista x64 pidgenx.dll was not found at:\n" << dllPath << L"\n";
        return 2;
    }
    attrs = GetFileAttributesW(configPath);
    if (attrs == INVALID_FILE_ATTRIBUTES) {
        std::wcerr << L"ERROR: Vista PKEY configuration was not found at:\n" << configPath << L"\n";
        return 3;
    }

    std::wcout << L"Vista PidGenX read-only checker (x64)\n"
               << L"Enter a key locally. It is not saved or transmitted.\n\n"
               << L"Product key: ";

    std::wstring key;
    std::getline(std::wcin, key);
    if (key.empty()) {
        std::wcerr << L"No key entered.\n";
        return 4;
    }
    if (key.size() >= 64) {
        std::wcerr << L"Input is too long.\n";
        return 5;
    }

    HMODULE module = LoadLibraryW(dllPath);
    if (!module) {
        std::wcerr << L"ERROR: LoadLibrary failed, Win32 error " << GetLastError() << L".\n";
        return 6;
    }

    PFN_PIDGENX pidgenx = reinterpret_cast<PFN_PIDGENX>(
        GetProcAddress(module, "PidGenX"));
    if (!pidgenx) {
        std::wcerr << L"ERROR: PidGenX export was not found, Win32 error "
                   << GetLastError() << L".\n";
        FreeLibrary(module);
        return 7;
    }

    // These sizes and the leading size markers follow the public KeyCheck
    // PidGenX wrapper: DPID2=0x32, DPID3=0xA4, DPID4=0x4F8 bytes.
    unsigned char pid[0x32] = { 0 };
    unsigned char dpid[0xA4] = { 0 };
    unsigned char dpid4[0x4F8] = { 0 };
    pid[0] = 0x32;
    dpid[0] = 0xA4;
    dpid4[0] = 0xF8;
    dpid4[1] = 0x04;

    WCHAR mspid[] = L"XXXXX";
    HRESULT result = pidgenx(&key[0], const_cast<WCHAR*>(configPath),
                             mspid, 0, pid, dpid, dpid4);

    std::cout << "\nPidGenX HRESULT: 0x" << std::hex << std::uppercase
              << static_cast<unsigned long>(result) << std::dec << "\n";

    if (result == 0) {
        std::cout << "Local PidGenX result: accepted by this installed DLL/config pair.\n";
        PrintField("Product ID: ", pid, 0, sizeof(pid));
        PrintField("Advanced PID: ", dpid4, 8, 128);
        PrintField("Activation ID: ", dpid4, 0x88, 128);
        PrintField("Edition type: ", dpid4, 0x118, 520);
        PrintField("Edition ID: ", dpid4, 0x378, 128);
        PrintField("Key type: ", dpid4, 0x3F8, 128);
        PrintField("EULA: ", dpid4, 0x478, 128);
        std::cout << "\nNote: this is an offline key/configuration check only; it does not prove ownership, "
                     "genuine licensing, or activation status.\n";
    } else if (static_cast<unsigned long>(result) == 0x80070057UL) {
        std::cout << "PidGenX reported invalid arguments. Check the DLL/config architecture and paths.\n";
    } else {
        std::cout << "PidGenX did not accept the key/config input. This may mean an invalid key, "
                     "wrong product family/config, or another local error.\n";
    }

    SecureZeroMemory(&key[0], key.size() * sizeof(wchar_t));
    FreeLibrary(module);
    std::cout << "\nPress Enter to exit...";
    std::string wait;
    std::getline(std::cin, wait);
    return result == 0 ? 0 : 1;
}
