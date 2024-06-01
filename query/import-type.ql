/**
 * @id java-kotlin/import-type
 * @name Import
 * @description Import Type
 * @kind problem
 * @problem.severity recommendation
 */

import java

from ImportType i
select i, i.getFile().getRelativePath() + " " + i.getImportedType().getQualifiedName()