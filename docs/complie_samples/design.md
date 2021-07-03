# The technical architecture of cga

## flow

```mermaid
flowchart TB

    subgraph codeblock
    _linked_list_node_4[code_start]
    _linked_list_node_4 --> _linked_list_node_5[text_line]
    _linked_list_node_5 --> _linked_list_node_6[code_end]
    end

    subgraph tokenlist
    _linked_list_header[h1] --> _linked_list_node_0[text_line]
    _linked_list_node_0 --> _linked_list_node_1[text_line]
    _linked_list_node_1 --> _linked_list_node_2[h2]
    _linked_list_node_2 --> _linked_list_node_3[text_line]
    _linked_list_node_3 --> codeblock
    codeblock x-. insert .-x _linked_list_node_7[h2]
    _linked_list_node_7 --> _linked_list_node_8[text_line]
    end

    subgraph lexer
    _lexer[lex]
    end
    
    subgraph parser
    _blocks_hunter[hunt]
    _insert[insert]
    end

    subgraph gener
    _generate[todoc]
    end

    subgraph cc-accessor
    _gcca[ca] -- code --> _gcc[gcc]
    _gcc --error info --> _gcca
    
    _gcca -- code --> _clang[clang]
    _clang -- error info --> _gcca

    _gcca -- code --> _msvc[msvc]
    _msvc -- error info --> _gcca
    end

    subgraph errorblock
    _error_info_header[h2] --> _error_info_node_1[text_line]
    _error_info_node_1 --> _error_info_node_2[code_start]
    _error_info_node_2 --> _error_info_node_3[text_line]
    _error_info_node_3 --> _error_info_node_4[text_line]
    _error_info_node_4 --> _error_info_node_5[code_end]
    end


    codeblock -- insert --> errorblock
    errorblock -- insert --> _linked_list_node_7

    codeblock ==> _blocks_hunter
    _blocks_hunter == code ==> cc-accessor ==> errorblock
    lexer ==> tokenlist

    tokenlist ==> gener
    _generate ==> _md_file[markdown]

```

```
+ Public
- Private
# Protected
~ Package/Internal
```

```json
[
    {"h2": "##"},
    {"text_line": "this is h2"},
    {"code_start": "```c"},
    {"text_line": "int main() {"},
    {"text_line": "    return 0;"},
    {"text_line": "}"},
    {"code_end": "```"}
]
```
