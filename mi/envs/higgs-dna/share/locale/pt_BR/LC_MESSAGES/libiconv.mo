��    -      �  =   �      �  C   �  9   %  o   _  B   �  m     ?   �  \   �  ;     P   Y  [   �       @   	  N   J  J   �  D   �  d   )  �   �  :   )	     d	     r	     {	  0   �	     �	  5   �	  	   
     
  )   "
  "   L
  1   o
  &   �
  A   �
  ;   
     F  /   V  7   �  3   �  :   �  ;   -  $   i     �     �     �     �  2   �  �    K     5   a  s   �  B     w   N  E   �  g     C   t  V   �  d        t  L   w  \   �  Z   !  T   |  q   �  �   C  :   �     '     7     @  >   `     �  0   �     �     �  1   �  (   +  9   T  +   �  H   �  <        @  E   Q  T   �  I   �  D   6  E   {  ,   �  $   �  &        :     H  >   V             #                                    $         (   -             +                                    	                &      !   '   *   ,                  
                  "          %      )            --byte-subst=FORMATSTRING   substitution for unconvertible bytes
   --help                      display this help and exit
   --unicode-subst=FORMATSTRING
                              substitution for unconvertible Unicode characters
   --version                   output version information and exit
   --widechar-subst=FORMATSTRING
                              substitution for unconvertible wide characters
   -c                          discard unconvertible characters
   -f ENCODING, --from-code=ENCODING
                              the encoding of the input
   -l, --list                  list the supported encodings
   -s, --silent                suppress error messages about conversion problems
   -t ENCODING, --to-code=ENCODING
                              the encoding of the output
 %s %s argument: A format directive with a size is not allowed here. %s argument: A format directive with a variable precision is not allowed here. %s argument: A format directive with a variable width is not allowed here. %s argument: The character '%c' is not a valid conversion specifier. %s argument: The character that terminates the format directive is not a valid conversion specifier. %s argument: The format string consumes more than one argument: %u argument. %s argument: The format string consumes more than one argument: %u arguments. %s argument: The string ends in the middle of a directive. %s: I/O error %s:%u:%u %s:%u:%u: cannot convert %s:%u:%u: incomplete character or shift sequence (stdin) Converts text from one encoding to another encoding.
 I/O error Informative output:
 Options controlling conversion problems:
 Options controlling error output:
 Options controlling the input and output format:
 Try '%s --help' for more information.
 Usage: %s [OPTION...] [-f ENCODING] [-t ENCODING] [INPUTFILE...]
 Usage: iconv [-c] [-s] [-f fromcode] [-t tocode] [file ...] Written by %s.
 cannot convert byte substitution to Unicode: %s cannot convert byte substitution to target encoding: %s cannot convert byte substitution to wide string: %s cannot convert unicode substitution to target encoding: %s cannot convert widechar substitution to target encoding: %s conversion from %s to %s unsupported conversion from %s unsupported conversion to %s unsupported or:    %s -l
 or:    iconv -l try '%s -l' to get the list of supported encodings Project-Id-Version: libiconv 1.15-pre1
Report-Msgid-Bugs-To: bug-gnu-libiconv@gnu.org
PO-Revision-Date: 2016-12-12 10:58-0200
Last-Translator: Rafael Fontenelle <rafaelff@gnome.org>
Language-Team: Brazilian Portuguese <ldpbr-translation@lists.sourceforge.net>
Language: pt_BR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1);
X-Generator: Virtaal 1.0.0-beta1
X-Bugs: Report translation errors to the Language-Team address.
   --byte-subst=TEXTOFORMATO   substituição para bytes não conversíveis
   --help                      exibe esta ajuda e sai
   --unicode-subst=TEXTOFORMATO
                              substituição de caracteres Unicode no conversíveis
   --version                   exibe informação da versão e sai
   --widechar-subst=TEXTOFORMATO
                              substituição para caracteres amplos não conversíveis
   -c                          descarta caracteres não conversíveis
   -f CODIFICAÇÃO, --from-code=CODIFICAÇÃO
                              a codificação de entrada
   -l, --list                  lista das codificações com suporte
   -s, --silent                suprime mensagens de erro sobre problemas de conversão
   -t CODIFICAÇÃO, --to-code=CODIFICAÇÃO
                              a codificação da saída
 %s argumento de %s: Uma diretiva de formato com um tamanho não permitida aqui. argumento de %s: Uma diretiva de formato com uma variável de precisão não permitida aqui. argumento de %s: Uma diretiva de formato com uma variável de largura não permitida aqui. argumento de %s: O caractere "%c" não é uma especificação de conversão válida. argumento de %s: O caractere que termina a diretiva de formato não é uma especificação de conversão válida. argumento de %s: O texto de formato consume mais do que um argumento: %u argumento. argumento de %s: O texto de formato consume mais do que um argumento: %u argumentos. argumento de %s: A string termina no meio de uma diretiva. %s: erro de E/S %s:%u:%u %s:%u:%u: impossível converter %s:%u:%u: sequência de caracteres ou deslocamentos incompleta (stdin) Converte texto de uma codificação para outra.
 erro de E/S Saída informativa:
 Opções para controlar problemas de conversão:
 Opções para controlar saída de erro:
 Opções para controlar os formatos de entrada e saída:
 Tente "%s --help" para mais informações.
 Uso: %s [OPÇÃO...] [-f CODIFICAÇÃO] [-t CODIFICAÇÃO] [ENTRADA...]
 Uso: iconv [-c] [-s] [-f fromcode] [-t tocode] [arquivo ...] Escrito por %s.
 não foi possível converter substituição de bytes para Unicode: %s não foi possível converter substituição de bytes para codificação desejada: %s não foi possível converter substituição de bytes para texto amplo: %s não foi possível converter unicode para codificação desejada: %s não foi possível converter widechar para codificação desejada: %s não há suporte à conversão de %s para %s não há suporte à conversão de %s não há suporte à conversão para %s ou:    %s -l
 ou:  iconv -l tente "%s -l" para obter a lista de codificações sem suporte 